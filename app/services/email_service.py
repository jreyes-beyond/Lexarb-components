from typing import Optional
import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi import HTTPException
import secrets
import string

class EmailService:
    """...[content from email-service artifact]"""
    # [Rest of the EmailService implementation]
