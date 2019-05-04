import yaml
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from datetime import datetime


def resend_verification_email(update_details, cosmo_user, verification_code):
    credentials = yaml.load(open('credentials.yaml'), Loader=yaml.FullLoader)
    sender = credentials['cosmo_admin_email']
    password = credentials['cosmo_admin_password']
    recipient = update_details['recipient_email']
    msg = MIMEText(update_details['email_body'])
    msg['Subject'] = update_details['email_subject']
    msg['From'] = sender
    msg['To'] = recipient

    try:
        server = smtplib.SMTP_SSL(credentials['smtp_server'], credentials['smtp_port'])
        server.login(sender, password)
        server.sendmail(sender, [recipient], msg.as_string())
        server.quit()
        cosmo_user.token = verification_code
        cosmo_user.resend_code = False
        cosmo_user.expiry = datetime.now()
        cosmo_user.save()
        return True
    except Exception as e:
        print(e)
        return False