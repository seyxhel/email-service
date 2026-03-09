"""
Django Admin configuration for the Customer Warning System.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Message


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ["id", "username", "email", "first_name", "last_name", "role", "is_active", "date_joined"]
    list_filter = ["role", "is_active", "date_joined"]
    search_fields = ["username", "email", "first_name", "last_name"]
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Role", {"fields": ("role", "phone")}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ("Role", {"fields": ("role", "phone")}),
    )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ["id", "sender", "recipient", "warning_type", "subject", "is_read", "created_at"]
    list_filter = ["warning_type", "is_read", "created_at"]
    search_fields = ["subject", "sender__username", "recipient__username"]
    readonly_fields = ["created_at", "read_at"]
    raw_id_fields = ["sender", "recipient"]
