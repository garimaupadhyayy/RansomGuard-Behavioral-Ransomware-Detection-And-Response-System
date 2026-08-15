"""
Email alerts via SMTP - fires when a high/critical severity incident happens.
"""
import smtplib
from email.mime.text import MIMEText
from app.settings import settings


def send_alert_email(subject: str, body: str) -> dict:
    if not settings.SMTP_HOST or not settings.ALERT_EMAIL_TO:
        return {"sent": False, "reason": "SMTP not configured in .env"}

    msg = MIMEText(body)
    msg["Subject"] = f"[RansomGuard] {subject}"
    msg["From"] = settings.SMTP_USERNAME
    msg["To"] = settings.ALERT_EMAIL_TO

    try:
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
            server.sendmail(settings.SMTP_USERNAME, [settings.ALERT_EMAIL_TO], msg.as_string())
        return {"sent": True}
    except smtplib.SMTPException as e:
        return {"sent": False, "reason": str(e)}
