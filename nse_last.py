# This module opens Nse page for each stock and checks when the trading last happened
# and returns that date. this helps to compare the date in db and fetch missed out
# stocks data accordingly

# import statements
import requests
from bs4 import BeautifulSoup
from datetime import date, datetime
from nse_download import get_scrip_list


def get_last(scrip):
    url = f"https://www.nseindia.com/live_market/dynaContent/live_watch/get_quote/GetQuote.jsp?symbol={scrip}"
           # "https://www1.nseindia.com/live_market/dynaContent/live_watch/get_quote/GetQuote.jsp?symbol=ABB"
    data = requests.get(url).content#.decode("utf-8")
    # data = BeautifulSoup(data, "html.parser").find("div", {"id": "responseDiv"}).text.strip()[15:24]
    # last_date = date.strftime(datetime.strptime(data, "%d%b%Y"), "%d-%m-%Y")
    return data


if __name__ == "__main__":

'''
https://www.nseindia.com/api/historical/cm/equity?symbol=COALINDIA&series=[%22EQ%22]&from=11-01-2019&to=11-01-2020&csv=true

https://www.nseindia.com/api/equity-stockIndices?csv=true&index=NIFTY%2050
https://www.nseindia.com/api/equity-stockIndices?csv=true&index=NIFTY%20100
'''
