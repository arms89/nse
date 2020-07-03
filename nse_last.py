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
               'Host': 'www1.nseindia.com',
               'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/83.0.4103.116 Safari/537.36'}

    session = requests.session()
    url = f"https://www1.nseindia.com/live_market/dynaContent/live_watch/get_quote/GetQuote.jsp?symbol={scrip}"
    session.headers.update(headers)
    data = session.get(url).content.decode('utf-8')
    data = BeautifulSoup(data, "html.parser").find("div", {"id": "responseDiv"}).text.strip()[15:24]
    last_date = date.strftime(datetime.strptime(data, "%d%b%Y"), "%d-%m-%Y")
    return last_date


if __name__ == "__main__":
    print(get_last_traded_date("ABB"))

'''
https://www.nseindia.com/api/historical/cm/equity?symbol=COALINDIA&series=[%22EQ%22]&from=11-01-2019&to=11-01-2020&csv=true
https://www.nseindia.com/api/equity-stockIndices?csv=true&index=NIFTY%2050
https://www.nseindia.com/api/equity-stockIndices?csv=true&index=NIFTY%20100
'''

