"""
Django Admin configuration for the Customer Warning System.
"""

from django.contrib import admin
from .models import Customer, WarningLog


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["id", "first_name", "last_name", "email", "phone", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["first_name", "last_name", "email"]
    readonly_fields = ["created_at", "updated_at"]


@admin.register(WarningLog)
class WarningLogAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "customer",
        "warning_type",
        "subject",
        "status",
        "sent_by",
        "sent_at",
        "created_at",
    ]
    list_filter = ["status", "warning_type", "created_at"]
    search_fields = [
        "customer__first_name",
        "customer__last_name",
        "customer__email",
        "subject",
    ]
    readonly_fields = [
        "sendgrid_message_id",
        "error_detail",
        "sent_at",
        "created_at",
    ]
    raw_id_fields = ["customer"]

    def has_change_permission(self, request, obj=None):
        # Warning logs are system-generated; prevent manual edits.
        return False
