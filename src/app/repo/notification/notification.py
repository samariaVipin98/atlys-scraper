import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email configuration

def send_email(to_email: str, subject: str, body: str):
    print(to_email, subject, body)
    msg = MIMEMultipart()
    msg['From'] = os.getenv("SENDER_EMAIL_ADDRESS")
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(os.getenv("SENDER_EMAIL_ADDRESS"), os.getenv("SENDER_EMAIL_PASSWORD"))
        server.send_message(msg)