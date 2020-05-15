# # Import Statements
# import pandas as ps
# from os import path, chdir, environ
# import datetime
#
#
# def signal(data):
#     """
#     Long = close[2] < open[2] and close[1] < open[1] and ohlc4[1] < ohlc4[2] and close > open and open < open[1]
#     Short = close[2] > open[2] and close[1] > open[1] and ohlc4[1] > ohlc4[2] and close < open and close < close[1]
#     """
#     price_filter = (data['OHLC'][0] and data['OHLC'][1]) >= 0
#     long_signal  = (data["Close Price"][2] < data["Open Price"][2] and
#                     data["Close Price"][1] < data["Open Price"][1] and
#                     data["OHLC"][1] < data["OHLC"][2] and
#                     data['Close Price'][0] > data['Open Price'][0] and
#                     data['Open Price'][0] < data['Open Price'][1] and
#                     price_filter)
#
#     short_signal = (data["Close Price"][2] > data["Open Price"][2] and
#                     data["Close Price"][1] > data["Open Price"][1] and
#                     data["OHLC"][1] > data["OHLC"][2] and
#                     data['Close Price'][0] < data['Open Price'][0] and
#                     data['Close Price'][0] < data['Close Price'][1] and
#                     price_filter)
#
#     # when LONG or SHORT signal gets generated they are returned in list format [date, script name, buy/sell]
#     if long_signal:
#         return [data['Date'][0], str(data["Symbol"][0]).replace('amp;', ''), "Buy"]
#     elif short_signal:
#         return [data['Date'][0], str(data["Symbol"][0]).replace('amp;', ''), "Sell"]
#     else:
#         return 0
#
#
# def main():
#     signal_list = []
#     today, sno = datetime.datetime.today().strftime('%d-%m-%Y'), 0
#     log_file = f'{str(today)}.log'
#
#     # if base Operating system is windows then OS name is nt else OS name is posix
#     # based on OS, navigate to the user's Downloads directory and also create a log file for tracking
#     if os.name == 'nt':
#         chdir(path.join(environ['USERPROFILE'], 'Downloads'))
#         # creating Log file to enter log of each processed file
#         log = open(log_file, 'w+')
#     elif os.name == 'posix':
#         chdir(path.join(environ['HOME'], 'Downloads'))
#         # creating Log file to enter log of each processed file
#         log = open(log_file, 'w+')
#
#     # once inside Downloads directory, open each stock's csv file and pull data in pandas data-frame format
#     for file in os.listdir():
#         # below if condition is to separate the stock data from other files in Downloads directory
#         if str(file).__contains__("-TO-") and str(file).__contains__("EQN.csv"):
#             data = ps.read_csv(file)[::-1].reset_index()
#
#             # drop unnecessary columns from the pulled data and create new column for
#             # OHLC(average of open, close, high and low)
#             data = data.drop(columns=["Series", "index", "Prev Close", "Last Price", "No. of Trades", "Turnover"])
#             data["OHLC"] = (data['Open Price'] + data['High Price'] + data['Low Price'] + data['Close Price'])/4
#
#             # call to signal() function to generate the signal
#             signals = signal(data)
#             if signals != 0:
#                 signal_list.append(signals)
#             sno += 1
#             log.write(f'{str(sno).zfill(3)} - {file.ljust(42)}- processed\n')
#             #os.remove(file)
#
#     with open('signals.csv', 'w+') as f:
#         f.write(','.join(['Date', 'Symbol', 'Buy_Sell']))
#         f.write('\n')
#         sig_list = sorted(signal_list, key=lambda x: x[1])
#         # Iterating through sorted signal list and writing the valuse in csv format into the signal.txt file
#         for i in sig_list:
#             values = ",".join(i)
#             f.write(f'{values}\n')
#
#     # terminating the open files
#     f.close()
#     log.close()
#
#
# if __name__ == "__main__":
#     main()
