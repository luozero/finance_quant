#-*- coding:UTF-8 -*-

import pandas as pd
import os

from stock_deeplearning.ultility.stock_codes_utility import stock_codes_utility as SCU
from stock_deeplearning.ultility.download_record import download_record as DR
from stock_deeplearning.ultility.common_func import nearest_date
from stock_deeplearning.ultility.common_def import * 
from stock_deeplearning.data_set.finance_data.financial_load_store import financial_load_store as FLD

class process_daily_trade_data(object):

  def __init__(self, path_root='../../../data/', stock_codes=['000001']):

    path = os.path.join(path_root, FOLDER_DATA_DOWNLOAD)
    if not os.path.exists(path):
      print("pls download finance data")
    self.file_daily_trade = os.path.join(path, FILE_DAILY_TRADE)

    # path = os.path.join(path_root, FOLDER_DAILY_TRADE_PROCESSED)
    # if not os.path.exists(path):
    #           os.makedirs(path)
    #self.path = path
    self.stock_file_daily_trade_quarter = os.path.join(path, FILE_DAILY_TRADE_QUARTER)

    self.DR = DR(path_root, JSON_FILE_PROCESS_RECORD, CSV_PROCESS_DAILY_TRADE_SKIP_STOCK)

    print("path stock trade data", path)
    self.FLD = FLD(path=path_root)

    self.proc_id = self.DR.read_data(KEY_PROCESS, KEY_PROCESS_DAILY_TRADE_QUARTER_INDEX)
    self.stock_codes = stock_codes[self.proc_id:]

  
  def processe_daily_trade_data_quarter(self):

    for stock_code in self.stock_codes:

      data_main = self.FLD.load_all_financial_one_stock(stock_code)
      finance_main = FILE_MAIN.format(stock_code)

      if data_main[finance_main].empty == True:

          print("no this stock", stock_code, "data")
          self.DR.write_skip_stock(stock_code)
      else:

        file_name = FILE_DAILY_TRADE.format(stock_code)

        dates = data_main[finance_main].columns[1:self.FLD.min_column]

        daily_trade_data = self.FLD.load_financical_data([file_name])[file_name]

        # no trade data skip this stock 
        # print(daily_trade_data)
        if (daily_trade_data.shape[0] == 0):
          print("no this stock", stock_code, "data")
          self.DR.write_skip_stock(stock_code)
          continue 

        daily_trade_dates = daily_trade_data.loc[:,'日期']
        trade_data_quarter = pd.DataFrame(columns=daily_trade_data.columns)
        # print('trade_data_quarter ', daily_trade_data.columns)
        times = 0
        for get_date in dates:
          times = times + 1
          # print(file_name, 'date is', get_date, 'fetch time', times)

          date_in_daily_trade_dates = nearest_date(daily_trade_dates, get_date)
          # print(daily_trade_data[date_in_daily_trade_dates == daily_trade_dates])
          # trade_data_quarter = trade_data_quarter.append(daily_trade_data[date_in_daily_trade_dates == daily_trade_dates])
          trade_data_quarter = pd.concat([trade_data_quarter, daily_trade_data[date_in_daily_trade_dates == daily_trade_dates]])

        # trade_data_quarter.index = dates
        file_csv = self.stock_file_daily_trade_quarter.format(stock_code)
        trade_data_quarter.to_csv(file_csv, encoding='gbk')
        print("store to ", file_csv)

        self.DR.write_data(KEY_PROCESS, KEY_PROCESS_DAILY_TRADE_QUARTER_INDEX, self.proc_id)
        self.proc_id = self.proc_id + 1
        print('this stock',stock_code, 'successfully downloaded')