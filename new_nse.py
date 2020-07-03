# Imports
import requests
import sqlite3
import os
import pandas as pd
from io import StringIO
from bs4 import BeautifulSoup
from datetime import date, datetime, timedelta


def setup_session():
    session = requests.session()
    headers = {'Accept': '*/*',
               'Accept-Encoding': 'gzip, deflate, br',
               'Accept-Language': 'en-US,en;q=0.9',
               'Connection': 'keep-alive',
               'Host': 'www.nseindia.com',
               'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/83.0.4103.116 Safari/537.36'}
    session.headers.update(headers)
    return session


def teardown_session(session):
    session.close()


def setup_db_connection():
    # setup db connection
    # if base Operating system is windows then OS name is nt else OS name is posix
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
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    return connection, cursor


def teardown_db_connection(connection):
    connection.commit()
    connection.close()


def get_last_traded_date(session, scrip):
    scrip = scrip.replace('&amp;', '%26')
    url = f"https://www.nseindia.com/api/historical/cm/equity?symbol={scrip}"
    data = session.get(url).content.decode('utf-8')
    data = data[data.find('"CH_TIMESTAMP":"') + 16:data.find('"CH_TIMESTAMP":"') + 26]
    last_traded_date = date.strftime(datetime.strptime(data, "%Y-%m-%d"), "%d-%m-%Y")
    return datetime.strptime(last_traded_date, '%d-%m-%Y')


def get_db_last_date(connection, cursor, scrip):
    scrip = scrip.replace('&', '&amp;')
    db_last_date = ''
    try:
        cursor.execute(f'select * from STOCKS where symbol like "{scrip}" order by date desc limit 1')
        last_row = cursor.fetchone()
        try:
            db_last_date = date.strftime(datetime.strptime(last_row[2], '%Y-%m-%d %H:%M:%S'), "%d-%m-%Y")
        except TypeError:
            pass
    except sqlite3.OperationalError:
        db_last_date = None
    return datetime.strptime(db_last_date, '%d-%m-%Y')


def fetch_historical(scrip):
    scrip = scrip.replace('&amp;', '%26')
    pass


def fetch_current(session, scrip, from_date, to_date):
    scrip = scrip.replace('&amp;', '%26')
    from_date = date.strftime(from_date + timedelta(1),
                              "%d-%m-%Y")
    to_date = date.strftime(to_date, "%d-%m-%Y")
    url = f'https://www.nseindia.com/api/historical/cm/equity?' \
          f'symbol={scrip}&series=[%22EQ%22]&from={from_date}&to={to_date}&csv=true'
    print(url)
    data = StringIO(session.get(url).content.decode())
    data = pd.read_csv(data, sep=',', parse_dates=['Date '])
    # data['Date'] = pd.to_datetime(data['Date'])
    return data


def main():
    scrip = 'ABB'
    session = setup_session()
    connection, cursor = setup_db_connection()
    last_traded_date = get_last_traded_date(session, scrip)
    db_last_date = get_db_last_date(connection, cursor, scrip)
    if last_traded_date > db_last_date:
        data = fetch_current(session, scrip, db_last_date, last_traded_date)
        print(data.info())
        print(data.head())
    elif last_traded_date is None:
        print('fetch historic')
        # fetch_historical(scrip)
    elif last_traded_date == db_last_date:
        print("DB already up-to date")
    teardown_db_connection(connection)
    teardown_session(session)


if __name__ == '__main__':
    main()
