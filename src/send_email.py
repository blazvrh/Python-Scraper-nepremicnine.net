""" Email sender """
from datetime import datetime
import smtplib
from email.mime.text import MIMEText

import config
import src.file_handler as file_handler
from config_mail_auth import gmail_user, gmail_password


class Email:
    """
    Email handler
    """
    def __init__(self):
        self.email_subject = config.Email.subject + " - " + datetime.now().strftime("%d.%m.%Y %H:%M")
        self.email_body = file_handler.get_file_content(config.output_file_path)
        self.recipients = config.Email.recipients

    def send_email(self):
        """
        Send email from a Gmail account

        :return: None
        """
        message = MIMEText(self.email_body, 'plain', 'utf-8')

        message['Subject'] = self.email_subject
        message['From'] = gmail_user
        message['To'] = ','.join(self.recipients)

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
