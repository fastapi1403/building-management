from typing import List, Optional
from fastapi import BackgroundTasks
from src.core.config import settings
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class NotificationService:
    async def send_email_notification(
        self,
        recipient: str,
        subject: str,
        body: str
    ) -
        # Email sending logic here
        pass

    async def send_sms_notification(
        self,
        phone: str,
        message: str
    ) -
        # SMS sending logic here
        pass
