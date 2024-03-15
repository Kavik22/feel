from config import USERNAME, HOST, PORT, PASSWORD
from ssl import create_default_context
from email.mime.text import MIMEText
from smtplib import SMTP
from validator import MailBodyValidator


def send_email(data: dict | None = None):
    msg = MailBodyValidator(**data)
    message = MIMEText(msg.body, 'html')
    message['From'] = USERNAME
    message['To'] = ','.join(msg.to)
    message['Subject'] = msg.subject

    ctx = create_default_context()

    try:
        with SMTP(HOST, PORT) as server:
            server.ehlo()
            server.starttls(context=ctx)
            server.ehlo()
            server.login(USERNAME, PASSWORD)
            server.send_message(message)
            server.quit()
            print({'status': 200, 'errors': None})
    except Exception as ex:
        print({'status': 500, 'errors': ex})

