# This module opens Nse page for each stock and checks when the trading last happened
# and returns that date. this helps to compare the date in db and fetch missed out
# stocks data accordingly

# import statements
import requests
from bs4 import BeautifulSoup
from datetime import date, datetime
from nse_download import get_scrip_list


def get_last_traded_date(scrip):
    headers = {'Accept': '*/*',
               'Accept-Encoding': 'gzip, deflate, br',
               'Accept-Language': 'en-US,en;q=0.9',
               'Connection': 'keep-alive',
               'Host': 'www.nseindia.com',
               'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/83.0.4103.116 Safari/537.36'}

    session = requests.session()
    url = f"https://www.nseindia.com/api/historical/cm/equity?symbol={scrip}"
    session.headers.update(headers)
    data = session.get(url).content.decode('utf-8')
    data = data[data.find('"CH_TIMESTAMP":"')+16:data.find('"CH_TIMESTAMP":"')+26]
    last_date = date.strftime(datetime.strptime(data, "%Y-%m-%d"), "%d-%m-%Y")
    return last_date


if __name__ == "__main__":
    print(get_last_traded_date("ABB"))
'''
https://www.nseindia.com/api/historical/cm/equity?symbol=COALINDIA&series=[%22EQ%22]&from=11-01-2019&to=11-01-2020&csv=true
https://www.nseindia.com/api/equity-stockIndices?csv=true&index=NIFTY%2050
https://www.nseindia.com/api/equity-stockIndices?csv=true&index=NIFTY%20100
'''
