"""Quick SendGrid diagnostic script."""
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv
import os

load_dotenv()

sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
msg = Mail(
    from_email="sethpelagio20@gmail.com",
    to_emails="ysah0510@gmail.com",
    subject="Test",
    plain_text_content="Test message",
)

try:
    response = sg.send(msg)
    print(f"SUCCESS: status={response.status_code}")
    print(f"body={response.body}")
except Exception as e:
    print(f"Exception type: {type(e).__name__}")
    print(f"Message: {e}")
    body = getattr(e, "body", None)
    status = getattr(e, "status_code", None)
    headers = getattr(e, "headers", None)
    print(f"Status code: {status}")
    print(f"Body: {body}")
    print(f"Headers: {headers}")
