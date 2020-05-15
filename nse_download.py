#!/usr/bin/env python3

from selenium import webdriver
from selenium.common import exceptions
import pandas as pd
import os
from pyautogui import hotkey
from time import sleep
import requests
import sqlite3 as sql
import io
from datetime import date, datetime, timedelta
# from nse_last import get_last

def get_scrip_list(qty=50):
    # gets the specific number of scripts from NSE website for eg. NIFTY50, NIFTY100, NIFTY200. Default is NIFTY100
    raw_csv_file = pd.read_csv(f'https://www.nseindia.com/api/equity-stockIndices?csv=true&index=NIFTY%2050')
    print(raw_csv_file)
    # scrip_file = pd.read_csv(io.StringIO(raw_csv_file.decode('utf-8')))
    # return scrip_file['Symbol'].tolist()


def setup_driver():
    # Setup the Driver and navigate to NSE url and set common field values.
    global driver
    driver.maximize_window()
    if os.name is 'posix':
        hotkey('command', 'ctrl', 'f')
    base_url = 'https://www1.nseindia.com/products/content/equities/equities/eq_security.htm'
    driver.implicitly_wait(5)
    driver.get(base_url)
    driver.find_element_by_id('dataType').send_keys('Security-wise Price volume & Deliverable position data')
    driver.find_element_by_id('series').send_keys('EQ')


def teardown_driver():
    # Teardown the web-driver
    global driver
    sleep(10)
    driver.quit()


def download_csv(scr):
    # Enters the Script name("scr") in the symbol field and download the csv file
    global driver
    driver.find_element_by_id('symbol').send_keys(scr)
    sleep(20)
    driver.find_element_by_id('get').click()
    driver.implicitly_wait(10)
    driver.find_element_by_link_text("Download file in csv format").click()
    sleep(5)
    driver.find_element_by_id('symbol').clear()


def setup_db_conn():
    # setup db connection
    # if base Operating system is windows then OS name is nt else OS name is posix
    # based on OS, navigate to the user's Downloads directory and also create a log file for tracking
    db_file = ""
    try:
        if os.name == 'nt':
            user_path = os.environ['USERPROFILE']
            db_file = user_path + r"\OneDrive\garbage\nse\stocks.db"
        elif os.name == 'posix':
            user_path = os.environ['HOME']
            if str(user_path).__contains__("saikrishna"):
                db_file = user_path + r"/OneDrive/garbage/nse/stocks.db"
            else:
                db_file = user_path + r"/nse_signals/stocks.db"
    except:
        print("Error occurred in setting/fetching the database")
    conn = sql.connect(db_file)
    cur = conn.cursor()
    return conn, cur


def teardown_db_conn(conn):
    conn.commit()
    conn.close()


def next_month(dt):
    if dt == 12:
        return 1
    else:
        return dt + 1


def parse_data():
    # if base Operating system is windows then OS name is nt else OS name is posix
    # based on OS, navigate to the user's Downloads directory and also create a log file for tracking
    try:
        if os.name == 'nt':
            os.chdir(os.path.join(os.environ['USERPROFILE'], 'Downloads'))

        elif os.name == 'posix':
            os.chdir(os.path.join(os.environ['HOME'], 'Downloads'))
    except:
        print("An error occurred while accessing/reading the downloaded csv data file of the stock")
    # once inside Downloads directory, open each stock's csv file and pull data in pandas data-frame format
    for file in os.listdir():
        # below if condition is to separate the stock data from other files in Downloads directory
        if str(file).__contains__("-TO-") and str(file).__contains__("EQN.csv"):
            data_ = pd.read_csv(file, parse_dates=['Date'])
            data_["Primarykey"] = data_['Symbol'] + data_["Date"].apply(lambda d: datetime.strftime(d, "%d-%m-%Y"))
            os.remove(file)
    return data_


def get_historic(scrip):
    # Loop for getting 10 years historic data, one year per iteration
    global driver
    driver.find_element_by_id('rdDateToDate').click()
    data = pd.DataFrame()
    for i in range(11, 0, -1):
        from_date = f'01-01-{date.today().year - i + 1}'

        if (date.today().year - i + 1) == date.today().year:
            to_date = f'{date.today().day:02}-{date.today().month:02}-{date.today().year - i + 1}'
        else:
            to_date = f'31-12-{date.today().year - i + 1}'
        driver.find_element_by_id('fromDate').send_keys(from_date)
        driver.find_element_by_id('toDate').send_keys(to_date)
        try:
            download_csv(scrip)
            data = data.append(parse_data())
        except exceptions.NoSuchElementException:
            print(f'from {from_date} till {to_date}: No data')
            driver.find_element_by_id('symbol').clear()
            driver.find_element_by_id('fromDate').clear()
            driver.find_element_by_id('toDate').clear()
        else:
            print(from_date, to_date, sep=" - ")
            driver.find_element_by_id('fromDate').clear()
            driver.find_element_by_id('toDate').clear()
    return data


def get_latest(scrip, last_date):
    global driver
    driver.find_element_by_id('rdDateToDate').click()
    data = pd.DataFrame()
    from_date = date.strftime(datetime.strptime(last_date, '%d-%m-%Y') + timedelta(1),
                              "%d-%m-%Y")
    to_date = f'{date.strftime(date.today(),"%d-%m-%Y")}'
    driver.find_element_by_id('fromDate').send_keys(from_date)
    driver.find_element_by_id('toDate').send_keys(to_date)
    try:
        download_csv(scrip)
        data = parse_data()
    except exceptions.NoSuchElementException:
        print(f'from {from_date} till {to_date}: No data')
        driver.find_element_by_id('symbol').clear()
        driver.find_element_by_id('fromDate').clear()
        driver.find_element_by_id('toDate').clear()
    else:
        print(from_date, to_date, sep=" - ")
        driver.find_element_by_id('fromDate').clear()
        driver.find_element_by_id('toDate').clear()
    return data


def main():
    global driver
    setup_driver()
    conn, cur = setup_db_conn()
    get_scrip_list()
    # Loop to get data for specified number of scrips (get_scrip_list(50 or 100 or 200)
    for scrip in get_scrip_list():
        scrip = scrip.replace('&', '&amp;')
        # scrip = scrip.replace("IDEA", "PGHH")
        try:
            cur.execute(f'select * from STOCKS where symbol like "{scrip}" order by date desc limit 1')
            last_row = cur.fetchone()
            try:
                has_date = date.strftime(datetime.strptime(last_row[2], '%Y-%m-%d %H:%M:%S'), "%d-%m-%Y")
            except TypeError:
                pass
        except sql.OperationalError:
            last_row = None
        # get last date of the scrip from NSE website
        scrip = scrip.replace('&amp;', '%26')
        # call get_last function to get latest date for current scrip, from NSE site

        latest_date = date.today()

        scrip = scrip.replace('%26', '&')

        # Below logic is to determine the fetch and update style based on already available data in db and
        # the latest date of the stock from the NSE site.
        # If last_row obtained from db is NONE, then stock is not present, so fetch all historic
        if last_row is None:
            print(f"{scrip} - Getting Historic data ", end=" - ")
            data = get_historic(scrip)
            data.to_sql("STOCKS", con=conn, if_exists="append", index=False)

        # else if Last_row is there and its already latest date then just display message
        elif has_date == latest_date:
            print(f'DB is already up-to-date for {scrip}...')

        # else if Last_row is there but its not the latest_date, then obtain only latest data from site.
        elif has_date != latest_date:
            print(f"{scrip} - Getting latest data ", end=" - ")
            data = get_latest(scrip, has_date)
            data.to_sql("STOCKS", con=conn, if_exists="append", index=False)

    # call Teardown driver function
    teardown_driver()
    # call Teardown db connection function
    teardown_db_conn(conn)


if __name__ == '__main__':
    print(get_scrip_list())

    # try:
        # if os.name == 'nt':
        #     user_path = os.environ['USERPROFILE']
        #     driver = webdriver.Chrome(f'{user_path}/OneDrive/garbage/nse/chromedriver.exe')
        # elif os.name == 'posix':
        #     driver = webdriver.Chrome('/Users/saikrishna/OneDrive/garbage/nse/chromedriver')

    # finally:
    #     # call Teardown driver function
    #     teardown_driver()