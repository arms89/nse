# Imports

from selenium import webdriver
import os
import pandas as pd
from datetime import timedelta, date
from sqlite3 import connect


class Nse:

    def __init__(self, scrip):
        self.scrip = scrip

    def setup_driver(self):
        if os.name == "nt":
            user_path = os.environ['USERPROFILE']
            self.driver = webdriver.Chrome(f"{user_path}/OneDrive/garbage/nse/chromedriver.exe")

    def tear_down_driver(self):
        self.driver.quit()

    def get_database_last_date(self):
        connection = connect("stocks.db")
        stock_data = pd.read_sql_query(
            f"select * from STOCKS where Symbol like '{self.scrip}' order by date desc limit 1",
            con=connection,
            parse_dates=['Date'])
        return date.strftime(stock_data['Date'][0] + pd.DateOffset(days=1), "%Y-%m-%d")

    def get_nse_last_date(self):

        pass

    def download_csv(self, scrip):
        pass


if __name__ == "__main__":
    obj = Nse('ZEEL')
    # obj.setup_driver()
    # obj.tear_down_driver()
    print(obj.get_database_last_date())
