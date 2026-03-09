"""
DRF Serializers for the Customer Warning System — in-app messaging.
"""

from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Message, WarningType

User = get_user_model()


# ---------- Auth ----------

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "phone", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
            phone=validated_data.get("phone", ""),
            password=validated_data["password"],
            role=User.Role.CUSTOMER,
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "phone", "role", "full_name", "date_joined"]
        read_only_fields = ["id", "role", "date_joined"]

    def get_full_name(self, obj):
        return obj.get_full_name() or obj.username


# ---------- Messages ----------

class MessageListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for inbox/sent list views."""
    sender_name = serializers.SerializerMethodField()
    recipient_name = serializers.SerializerMethodField()
    warning_type_display = serializers.CharField(source="get_warning_type_display", read_only=True)

    class Meta:
        model = Message
        fields = [
            "id", "sender", "sender_name", "recipient", "recipient_name",
            "warning_type", "warning_type_display", "subject",
            "is_read", "read_at", "created_at",
        ]

    def get_sender_name(self, obj):
        return obj.sender.get_full_name() or obj.sender.username if obj.sender else "System"

    def get_recipient_name(self, obj):
        return obj.recipient.get_full_name() or obj.recipient.username


class MessageDetailSerializer(serializers.ModelSerializer):
    """Full serializer with body for detail view."""
    sender_name = serializers.SerializerMethodField()
    recipient_name = serializers.SerializerMethodField()
    warning_type_display = serializers.CharField(source="get_warning_type_display", read_only=True)

    class Meta:
        model = Message
        fields = [
            "id", "sender", "sender_name", "recipient", "recipient_name",
            "warning_type", "warning_type_display", "subject", "body",
            "is_read", "read_at", "created_at",
        ]

    def get_sender_name(self, obj):
        return obj.sender.get_full_name() or obj.sender.username if obj.sender else "System"

    def get_recipient_name(self, obj):
        return obj.recipient.get_full_name() or obj.recipient.username


class SendMessageSerializer(serializers.Serializer):
    """Serializer for the send-message endpoint (staff only)."""
    recipient_id = serializers.IntegerField()
    warning_type = serializers.ChoiceField(choices=WarningType.choices)
    subject = serializers.CharField(max_length=255)
    body = serializers.CharField()

    def validate_recipient_id(self, value):
        try:
            user = User.objects.get(pk=value)
            if user.role != User.Role.CUSTOMER:
                raise serializers.ValidationError("Recipient must be a customer.")
        except User.DoesNotExist:
            raise serializers.ValidationError("Customer not found.")
        return value


class WarningTypeSerializer(serializers.Serializer):
    value = serializers.CharField()
    label = serializers.CharField()
