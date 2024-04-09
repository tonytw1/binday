from datetime import date
import requests
import pytz
from dateutil.parser import parse


def get_bindays(uprn):
    api_url = 'https://online.bcpcouncil.gov.uk/bcp-apis/?api=BinDayLookup&uprn=' + uprn
    print(api_url)
    r = requests.get(api_url)
    if r.status_code != 200:
        print(r.status_code)
        return None
    return r.json


def tommorows_bins(bins):
    return list(filter(collected_tommorow, bins))


def collected_tommorow(bin):
    # 4/9/2024 11:00:00 PM should resolve to 10 April 2024
    # The date format is mouth/day/year.
    # The time is midnight expressed as UTC
    # We need to convert that back to BST to get the correct new day midnight falls on
    next_collection_time = parse(bin['Next'])

    utc_tz = pytz.timezone('Etc/UTC')
    next_collection_time_utc = utc_tz.localize(next_collection_time)

    europe_london_tz = pytz.timezone('Europe/London')
    next_collection_time_bts = next_collection_time_utc.astimezone(europe_london_tz)
    next_collection_date = next_collection_time_bts.date()

    today = date.today()
    delta = (next_collection_date - today).days
    return delta == 1
