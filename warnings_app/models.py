"""
Database models for the Customer Warning System.
"""

from django.db import models
from django.utils import timezone


class Customer(models.Model):
    """A customer record entered by staff."""

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, default="")
    notes = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class WarningType(models.TextChoices):
    """Predefined warning categories."""

    OVERDUE = "overdue", "Overdue Notice"
    REMINDER = "reminder", "Reminder"
    FINAL_NOTICE = "final_notice", "Final Notice"
    POLICY_VIOLATION = "policy_violation", "Policy Violation"
    GENERAL = "general", "General Warning"


class WarningLog(models.Model):
    """Log of every warning email sent to a customer."""

    class DeliveryStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        SENT = "sent", "Sent"
        DELIVERED = "delivered", "Delivered"
        FAILED = "failed", "Failed"

    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="warnings"
    )
    warning_type = models.CharField(
        max_length=30,
        choices=WarningType.choices,
        default=WarningType.GENERAL,
    )
    subject = models.CharField(max_length=255)
    message = models.TextField(help_text="Body of the warning email.")
    status = models.CharField(
        max_length=15,
        choices=DeliveryStatus.choices,
        default=DeliveryStatus.PENDING,
    )
    sendgrid_message_id = models.CharField(max_length=255, blank=True, default="")
    error_detail = models.TextField(blank=True, default="")
    sent_by = models.CharField(
        max_length=150,
        blank=True,
        default="",
        help_text="Username of the staff member who triggered the warning.",
    )
    sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"[{self.get_warning_type_display()}] → {self.customer.email} ({self.status})"

    def mark_sent(self, message_id: str = ""):
        self.status = self.DeliveryStatus.SENT
        self.sendgrid_message_id = message_id
        self.sent_at = timezone.now()
        self.save(update_fields=["status", "sendgrid_message_id", "sent_at"])

    def mark_failed(self, error: str = ""):
        self.status = self.DeliveryStatus.FAILED
        self.error_detail = error
        self.save(update_fields=["status", "error_detail"])
