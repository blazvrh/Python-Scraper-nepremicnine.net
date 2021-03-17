import smtplib
from email.mime.text import MIMEText
from config_mail_auth import gmail_user, gmail_password


def send_email(recipients: list, subject: str, body: str):
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
        print('Something went wrong...')
        print(err)
        import traceback
        traceback.print_tb(err.__traceback__)


if __name__ == "__main__":
    send_email(
        recipients=['blaz.vrhovec@gmail.com'],
        subject="New apartments",
        body="TesTT with a žšćčđ€[]"
    )
