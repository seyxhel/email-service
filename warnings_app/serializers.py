"""
DRF Serializers for the Customer Warning System.
"""

from rest_framework import serializers
from .models import Customer, WarningLog, WarningType


class CustomerSerializer(serializers.ModelSerializer):
    warning_count = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "phone",
            "notes",
            "warning_count",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def get_warning_count(self, obj):
        return obj.warnings.count()


class WarningLogSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source="customer.full_name", read_only=True)
    customer_email = serializers.CharField(source="customer.email", read_only=True)
    warning_type_display = serializers.CharField(
        source="get_warning_type_display", read_only=True
    )
    status_display = serializers.CharField(
        source="get_status_display", read_only=True
    )

    class Meta:
        model = WarningLog
        fields = [
            "id",
            "customer",
            "customer_name",
            "customer_email",
            "warning_type",
            "warning_type_display",
            "subject",
            "message",
            "status",
            "status_display",
            "sendgrid_message_id",
            "error_detail",
            "sent_by",
            "sent_at",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "status",
            "sendgrid_message_id",
            "error_detail",
            "sent_at",
            "created_at",
        ]


class SendWarningSerializer(serializers.Serializer):
    """Serializer for the send-warning endpoint."""

    customer_id = serializers.IntegerField()
    warning_type = serializers.ChoiceField(choices=WarningType.choices)
    subject = serializers.CharField(max_length=255)
    message = serializers.CharField()

    def validate_customer_id(self, value):
        try:
            Customer.objects.get(pk=value)
        except Customer.DoesNotExist:
            raise serializers.ValidationError("Customer not found.")
        return value


class WarningTypeSerializer(serializers.Serializer):
    """Returns available warning types."""

    value = serializers.CharField()
    label = serializers.CharField()
