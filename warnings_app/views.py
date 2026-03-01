"""
API views for the Customer Warning System.
"""

from rest_framework import viewsets, status, filters
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Customer, WarningLog, WarningType
from .serializers import (
    CustomerSerializer,
    WarningLogSerializer,
    SendWarningSerializer,
    WarningTypeSerializer,
)
from .email_service import send_warning_email


class CustomerViewSet(viewsets.ModelViewSet):
    """
    CRUD endpoints for customer records.

    list:    GET    /api/customers/
    create:  POST   /api/customers/
    read:    GET    /api/customers/{id}/
    update:  PUT    /api/customers/{id}/
    partial: PATCH  /api/customers/{id}/
    delete:  DELETE /api/customers/{id}/
    """

    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["first_name", "last_name", "email"]
    ordering_fields = ["created_at", "last_name", "email"]

    @action(detail=True, methods=["get"])
    def warnings(self, request, pk=None):
        """GET /api/customers/{id}/warnings/ — list warnings for a customer."""
        customer = self.get_object()
        warnings = customer.warnings.all()
        page = self.paginate_queryset(warnings)
        if page is not None:
            serializer = WarningLogSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = WarningLogSerializer(warnings, many=True)
        return Response(serializer.data)


class WarningLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only endpoints for warning logs.

    list: GET /api/warnings/
    read: GET /api/warnings/{id}/
    """

    queryset = WarningLog.objects.select_related("customer").all()
    serializer_class = WarningLogSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        "customer__first_name",
        "customer__last_name",
        "customer__email",
        "subject",
        "warning_type",
    ]
    ordering_fields = ["created_at", "sent_at", "status"]


@api_view(["POST"])
@permission_classes([AllowAny])
def send_warning(request):
    """
    POST /api/send-warning/

    Send a warning email to a customer. Creates a WarningLog entry,
    dispatches the email via SendGrid, and returns the result.

    Body:
        customer_id  (int)    — ID of the target customer
        warning_type (string) — one of: overdue, reminder, final_notice,
                                 policy_violation, general
        subject      (string) — email subject line
        message      (string) — email body text
    """
    serializer = SendWarningSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    data = serializer.validated_data
    customer = Customer.objects.get(pk=data["customer_id"])

    # Create the warning log entry
    warning_log = WarningLog.objects.create(
        customer=customer,
        warning_type=data["warning_type"],
        subject=data["subject"],
        message=data["message"],
        sent_by=request.user.username if request.user.is_authenticated else "system",
    )

    # Send the email
    success = send_warning_email(warning_log)

    # Refresh from DB after email_service updates the record
    warning_log.refresh_from_db()
    result_serializer = WarningLogSerializer(warning_log)

    return Response(
        {
            "success": success,
            "warning": result_serializer.data,
        },
        status=status.HTTP_201_CREATED if success else status.HTTP_502_BAD_GATEWAY,
    )


@api_view(["GET"])
@permission_classes([AllowAny])
def warning_types(request):
    """
    GET /api/warning-types/

    Return the list of available warning types.
    """
    types = [{"value": choice[0], "label": choice[1]} for choice in WarningType.choices]
    return Response(types)


@api_view(["GET"])
@permission_classes([AllowAny])
def dashboard_stats(request):
    """
    GET /api/stats/

    Return summary statistics for the staff dashboard.
    """
    from django.db.models import Count, Q

    total_customers = Customer.objects.count()
    total_warnings = WarningLog.objects.count()
    sent = WarningLog.objects.filter(status="sent").count()
    failed = WarningLog.objects.filter(status="failed").count()
    pending = WarningLog.objects.filter(status="pending").count()

    by_type = (
        WarningLog.objects.values("warning_type")
        .annotate(count=Count("id"))
        .order_by("-count")
    )

    return Response(
        {
            "total_customers": total_customers,
            "total_warnings": total_warnings,
            "sent": sent,
            "failed": failed,
            "pending": pending,
            "by_type": list(by_type),
        }
    )
