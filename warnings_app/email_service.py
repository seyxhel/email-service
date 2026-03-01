"""
SendGrid email service for sending customer warning emails.
"""

import logging
from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content

logger = logging.getLogger(__name__)


def send_warning_email(warning_log) -> bool:
    """
    Send a warning email via SendGrid and update the WarningLog record.

    Args:
        warning_log: A WarningLog model instance (must be saved already).

    Returns:
        True if the email was accepted by SendGrid, False otherwise.
    """
    api_key = settings.SENDGRID_API_KEY
    if not api_key:
        error_msg = "SENDGRID_API_KEY is not configured."
        logger.error(error_msg)
        warning_log.mark_failed(error_msg)
        return False

    message = Mail(
        from_email=settings.DEFAULT_FROM_EMAIL,
        to_emails=warning_log.customer.email,
        subject=warning_log.subject,
        plain_text_content=warning_log.message,
        html_content=_build_html_body(warning_log),
    )

    try:
        sg = SendGridAPIClient(api_key)
        response = sg.send(message)

        if response.status_code in (200, 201, 202):
            msg_id = response.headers.get("X-Message-Id", "")
            warning_log.mark_sent(message_id=msg_id)
            logger.info(
                "Warning email sent to %s (id=%s)",
                warning_log.customer.email,
                msg_id,
            )
            return True
        else:
            error_msg = f"SendGrid returned status {response.status_code}: {response.body}"
            logger.warning(error_msg)
            warning_log.mark_failed(error_msg)
            return False

    except Exception as exc:
        # Extract the response body from SendGrid exceptions for better diagnostics
        body = getattr(exc, "body", None) or ""
        status_code = getattr(exc, "status_code", None) or ""
        error_msg = (
            f"SendGrid API error (status={status_code}): {exc}\n"
            f"Response body: {body}"
        )
        logger.exception(error_msg)
        warning_log.mark_failed(error_msg)
        return False


def _build_html_body(warning_log) -> str:
    """Build a simple HTML email body following deliverability best practices."""
    return f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="utf-8"></head>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
        <h2 style="color: #2c3e50;">{warning_log.subject}</h2>
        <p>Dear {warning_log.customer.full_name},</p>
        <div style="background: #f9f9f9; border-left: 4px solid #2c3e50; padding: 15px; margin: 20px 0;">
            {warning_log.message.replace(chr(10), '<br>')}
        </div>
        <p style="font-size: 0.9em; color: #555;">
            Notice Type: {warning_log.get_warning_type_display()}
        </p>
        <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
        <p style="font-size: 0.8em; color: #999;">
            This message was sent by the Customer Notice System.<br>
            If you believe you received this in error, please contact us by replying to this email.<br>
            &copy; 2026 Customer Notice System
        </p>
    </div>
</body>
</html>"""
