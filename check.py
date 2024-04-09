import os
import smtplib
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import bcpapi

uprn = os.environ.get('UPRN')
message_from = os.environ.get('EMAIL_FROM')
message_to = os.environ.get('EMAIL_TO')
smtp_user = os.environ.get('SMTP_USER')
smtp_password = os.environ.get('SMTP_PASSWORD')
smtp_server = os.environ.get('SMTP_HOST')


def send_email(text):
    message = MIMEMultipart("alternative")
    message["Subject"] = "Bin day is coming"
    message["From"] = message_from
    message["To"] = message_to

    plain_part = MIMEText(text, "plain")
    message.attach(plain_part)

    server = smtplib.SMTP(smtp_server, 587)
    server.login(smtp_user, smtp_password)
    server.sendmail(message_from, message_to, message.as_string())


bins = bcpapi.get_bindays(uprn)
if bins is None:
    sys.exit(1)

tommorows_bins = bcpapi.tommorows_bins(bins)
if len(tommorows_bins) != 0:
    types = list(map(lambda b: b['BinType'], tommorows_bins))
    content = ', '.join(types)
    print(content)
    send_email(content)

print("Done")
