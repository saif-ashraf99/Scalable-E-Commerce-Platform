import smtplib
from email.mime.text import MIMEText
from twilio.rest import Client
import os

def send_email(to, subject, body):
    # Using SMTP (e.g., SendGrid or AWS SES)
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = os.getenv('EMAIL_FROM')
    msg['To'] = to
    
    with smtplib.SMTP(
        os.getenv('SMTP_HOST'), 
        os.getenv('SMTP_PORT')
    ) as server:
        server.login(
            os.getenv('SMTP_USER'),
            os.getenv('SMTP_PASSWORD')
        )
        server.send_message(msg)

def send_sms(phone_number, message):
    # Using Twilio
    client = Client(
        os.getenv('TWILIO_ACCOUNT_SID'),
        os.getenv('TWILIO_AUTH_TOKEN')
    )
    client.messages.create(
        body=message,
        from_=os.getenv('TWILIO_PHONE_NUMBER'),
        to=phone_number
    )

def send_push_notification(user_id, title, message):
    # Implement with Firebase Cloud Messaging or similar
    pass