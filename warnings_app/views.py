"""
API views for the Customer Warning System — in-app messaging.
"""

from django.contrib.auth import authenticate, login, logout, get_user_model
from django.db.models import Q
from rest_framework import status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Message, WarningType
from .serializers import (
    RegisterSerializer,
    UserSerializer,
    MessageListSerializer,
    MessageDetailSerializer,
    SendMessageSerializer,
)

User = get_user_model()


# ==================== Auth ====================

@api_view(["POST"])
@permission_classes([AllowAny])
def register_customer(request):
    """POST /api/auth/register/ — Create a new customer account."""
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    login(request, user)
    return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    """POST /api/auth/login/ — Log in with username & password."""
    username = request.data.get("username", "")
    password = request.data.get("password", "")
    user = authenticate(request, username=username, password=password)
    if user is None:
        return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
    login(request, user)
    return Response(UserSerializer(user).data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """POST /api/auth/logout/"""
    logout(request)
    return Response({"detail": "Logged out."})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me_view(request):
    """GET /api/auth/me/ — Return the current logged-in user."""
    return Response(UserSerializer(request.user).data)


# ==================== Customers (staff only) ====================

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def customer_list(request):
    """GET /api/customers/ — Staff: list all customer accounts."""
    if request.user.role != User.Role.STAFF:
        return Response({"detail": "Staff only."}, status=status.HTTP_403_FORBIDDEN)
    search = request.query_params.get("search", "")
    qs = User.objects.filter(role=User.Role.CUSTOMER)
    if search:
        qs = qs.filter(
            Q(first_name__icontains=search)
            | Q(last_name__icontains=search)
            | Q(username__icontains=search)
            | Q(email__icontains=search)
        )
    users = qs.order_by("-date_joined")
    return Response(UserSerializer(users, many=True).data)


# ==================== Messages ====================

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def inbox(request):
    """GET /api/inbox/ — Customer: list received messages. Staff: list all sent messages."""
    user = request.user
    if user.role == User.Role.CUSTOMER:
        messages = Message.objects.filter(recipient=user)
    else:
        messages = Message.objects.filter(sender=user)
    return Response(MessageListSerializer(messages, many=True).data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def message_detail(request, pk):
    """GET /api/messages/<id>/ — View a single message. Auto-marks as read for recipient."""
    try:
        msg = Message.objects.get(pk=pk)
    except Message.DoesNotExist:
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    # Only sender or recipient can view
    if request.user.id not in (msg.sender_id, msg.recipient_id):
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    # Auto-mark read when recipient opens it
    if request.user.id == msg.recipient_id:
        msg.mark_read()

    return Response(MessageDetailSerializer(msg).data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def send_message(request):
    """
    POST /api/send-message/ — Staff sends a warning/notice to a customer.

    Body: { recipient_id, warning_type, subject, body }
    """
    if request.user.role != User.Role.STAFF:
        return Response({"detail": "Staff only."}, status=status.HTTP_403_FORBIDDEN)

    serializer = SendMessageSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data

    recipient = User.objects.get(pk=data["recipient_id"])
    msg = Message.objects.create(
        sender=request.user,
        recipient=recipient,
        warning_type=data["warning_type"],
        subject=data["subject"],
        body=data["body"],
    )
    return Response(MessageDetailSerializer(msg).data, status=status.HTTP_201_CREATED)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def warning_types(request):
    """GET /api/warning-types/"""
    types = [{"value": c[0], "label": c[1]} for c in WarningType.choices]
    return Response(types)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    """GET /api/stats/ — Staff dashboard stats."""
    if request.user.role != User.Role.STAFF:
        return Response({"detail": "Staff only."}, status=status.HTTP_403_FORBIDDEN)

    from django.db.models import Count

    total_customers = User.objects.filter(role=User.Role.CUSTOMER).count()
    total_messages = Message.objects.count()
    unread = Message.objects.filter(is_read=False).count()
    read = Message.objects.filter(is_read=True).count()

    by_type = (
        Message.objects.values("warning_type")
        .annotate(count=Count("id"))
        .order_by("-count")
    )

    return Response({
        "total_customers": total_customers,
        "total_messages": total_messages,
        "unread": unread,
        "read": read,
        "by_type": list(by_type),
    })
