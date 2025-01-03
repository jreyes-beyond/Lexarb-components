from typing import Optional
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings
import aiosmtplib

class EmailService:
    def __init__(self, smtp_settings: dict = settings.SMTP):
        self.smtp_settings = smtp_settings

    async def send_document_request(self, case_email: str, request_id: str, description: str) -> None:
        """Send document request email."""
        subject = f"Document Request - {request_id}"
        body = f"""A new document has been requested for your case.

Request ID: {request_id}
Description: {description}

Please reply to this email with the requested document attached.
"""

        await self.send_email(case_email, subject, body)

    async def send_email(self, to_email: str, subject: str, body: str) -> None:
        """Send email using configured SMTP settings."""
        message = MIMEMultipart()
        message["From"] = self.smtp_settings["username"]
        message["To"] = to_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        async with aiosmtplib.SMTP(
            hostname=self.smtp_settings["host"],
            port=self.smtp_settings["port"],
            use_tls=self.smtp_settings["use_tls"]
        ) as smtp:
            await smtp.login(
                self.smtp_settings["username"],
                self.smtp_settings["password"]
            )
            await smtp.send_message(message)