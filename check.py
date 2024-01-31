import os
import requests
from datetime import date
from dateutil.parser import parse

uprn = os.environ.get('UPRN')
api_url = 'https://online.bcpcouncil.gov.uk/bcp-apis/?api=BinDayLookup&uprn=' + uprn
print(api_url)

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
    print(', '.join(types))

print("Done")
