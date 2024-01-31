import os
import requests
from datetime import date
from dateutil.parser import parse
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

uprn = os.environ.get('UPRN')
message_from = os.environ.get('EMAIL_FROM')
message_to = os.environ.get('EMAIL_TO')
smtp_user = os.environ.get('SMTP_USER')
smtp_password = os.environ.get('SMTP_PASSWORD')
smtp_server = os.environ.get('SMTP_HOST')

api_url = 'https://online.bcpcouncil.gov.uk/bcp-apis/?api=BinDayLookup&uprn=' + uprn
print(api_url)

def send_email(text):
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = message_from
    message["To"] = message_to

    plain_part = MIMEText(text, "plain")
    message.attach(plain_part)

    server = smtplib.SMTP(smtp_server, 587)
    server.login(smtp_user, smtp_password)
    server.sendmail(message_from, message_to, message.as_string())

def collected_tommorow(bin):
    today = date.today()
    next = bin['Next']
    nt = parse(next)
    delta = (nt.date() - today).days
    return delta == 1

r = requests.get(api_url)
if r.status_code != 200:
    print(r.status_code)
    exit()

data = r.json()
print(data)

tommorows_bins = list(filter(collected_tommorow, data))
if len(tommorows_bins) != 0:
    types = list(map(lambda b: b['BinType'], tommorows_bins))
    content = ', '.join(types)
    print(content)
    send_email(content)

print("Done")
