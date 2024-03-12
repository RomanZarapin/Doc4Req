import os
from email.message import EmailMessage
import aiosmtplib


async def send_reset_password(email: str, data: str):
    message = EmailMessage()
    message['From'] = os.getenv('MAIL_FROM_NAME', 'noreply@example.org')
    message['To'] = email
    message['Subject'] = 'Восстановление пароля'
    message.set_content(data, subtype='html')

    await aiosmtplib.send(
        message,
        hostname=os.getenv('MAIL_HOST'),
        port=os.getenv('MAIL_PORT'),
        username=os.getenv('MAIL_USERNAME', None),
        password=os.getenv('MAIL_PASSWORD', None),
        use_tls=bool(os.getenv('MAIL_USE_SSL', False)),
    )
