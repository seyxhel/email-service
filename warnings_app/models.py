"""
Database models for the Customer Warning System — in-app messaging.
"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    """Custom user model supporting both staff and customer roles."""

    class Role(models.TextChoices):
        STAFF = "staff", "Staff"
        CUSTOMER = "customer", "Customer"

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.CUSTOMER,
    )
    phone = models.CharField(max_length=20, blank=True, default="")

    class Meta:
        ordering = ["-date_joined"]

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.role})"

    @property
    def is_staff_role(self):
        return self.role == self.Role.STAFF

    @property
    def is_customer_role(self):
        return self.role == self.Role.CUSTOMER


class WarningType(models.TextChoices):
    """Predefined warning categories."""

    OVERDUE = "overdue", "Overdue Notice"
    REMINDER = "reminder", "Reminder"
    FINAL_NOTICE = "final_notice", "Final Notice"
    POLICY_VIOLATION = "policy_violation", "Policy Violation"
    GENERAL = "general", "General Warning"


class Message(models.Model):
    """An in-app message (warning/notice) sent from staff to a customer."""

    sender = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True,
        related_name="sent_messages",
    )
    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="received_messages",
    )
    warning_type = models.CharField(
        max_length=30,
        choices=WarningType.choices,
        default=WarningType.GENERAL,
    )
    subject = models.CharField(max_length=255)
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"[{self.get_warning_type_display()}] {self.subject} → {self.recipient}"

    def mark_read(self):
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save(update_fields=["is_read", "read_at"])
