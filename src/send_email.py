""" Email sender """
import smtplib
from email.mime.text import MIMEText

from config_mail_auth import gmail_user, gmail_password


def send_email(recipients: list, subject: str, body: str):
    """
    Send email from a Gmail account
    :param recipients: list[str]
    :param subject: str
    :param body: str (can include utf-16 characters)
    :return: None
    """
    message = MIMEText(body, 'plain', 'utf-8')

    message['Subject'] = subject
    message['From'] = gmail_user
    message['To'] = ','.join(recipients)

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()

        server.login(gmail_user, gmail_password)

        server.sendmail(message['From'], message['To'], message.as_string())

        server.close()

        print('Email sent!')
    except Exception as err:
        # TODO Write error to log file
        raise err
