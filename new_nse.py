# Imports
import requests as req
import pandas as pd
from io import StringIO

session = req.session()
headers = {'Accept': '*/*',
               'Accept-Encoding': 'gzip, deflate, br',
               'Accept-Language': 'en-US,en;q=0.9',
               'Connection': 'keep-alive',
               'Host': 'www.nseindia.com',
               'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/83.0.4103.116 Safari/537.36'}
session.headers.update(headers)
url = 'https://www.nseindia.com/api/historical/cm/equity?' \
      'symbol=COALINDIA&series=[%22EQ%22]&from=11-01-2019&to=11-01-2020&csv=true'
data = StringIO(session.get(url).content.decode('utf-8'))
raw = pd.read_csv(data, sep=',')
print(raw)


def setup_session():
    pass


def teardown_session():
    pass


def setup_db_connection():
    pass


def teardown_db_connection():
    pass


def fetch_historical(scrip):
    pass


def fetch_current(scrip):
    pass


def get_last_traded_date(scrip):
    pass


def get_db_last_date(scrip):
    pass


def main():
    setup_session()
    setup_db_connection()
    last_traded_date = get_last_traded_date(scrip)
    db_last_date = get_db_last_date(scrip)
    if last_traded_date > db_last_date:
        fetch_current(scrip)
    elif last_traded_date is None:
        fetch_historical(scrip)
    elif last_traded_date == current_date:
        print("DB already up-to date")
    teardown_db_connection()
    teardown_session()


if __name__ == '__main__':
    main()
