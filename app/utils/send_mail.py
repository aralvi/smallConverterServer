import smtplib
from email.message import EmailMessage
from email.utils import make_msgid
import ssl
from app.config.config import settings


def send_mail(reciever, subject, message=None, html=None):
    try:
        # Configuring Email
        mail = EmailMessage()
        mail["From"] = f"SmallConverterTools <{settings.MAIL}>"
        mail["To"] = reciever
        mail["Subject"] = subject
        if message:
            mail.set_content(message)
        if html:
            asparagus_cid = make_msgid()
            mail.add_alternative(html.format(
                asparagus_cid=asparagus_cid[1:-1]), subtype='html')
        context = ssl.create_default_context()
        # Configuring Server
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context)
        server.ehlo()
        server.login(settings.MAIL, settings.MAIL_PASS)
        server.sendmail(settings.MAIL, reciever, mail.as_string())
        server.close()
    except Exception as error:
        print('Something went wrong... (here in send_mail)')
        print(error)
