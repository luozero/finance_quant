#-*- coding:UTF-8 -*-

import pandas as pd
import numpy as np
import os

from ultility.stock_codes_utility import stock_codes_utility as SCU
from ultility.download_record import download_record as DR
from ultility.common_func import nearest_date
from ultility.common_def import * 
from data_set.finance_data.financial_load_store import financial_load_store as FLD

class process_daily_trade_data(object):

  def __init__(self, path_root='../../../data/', stock_codes=['000001'], data_type = TYPE_STOCK):

    path = os.path.join(path_root, FOLDER_DATA_DOWNLOAD)
    if not os.path.exists(path):
      print("pls download finance data")

    #self.path = path
    self.stock_file_daily_trade_quarter = os.path.join(path, FILE_DAILY_TRADE_QUARTER)

    stock_folder_daily_trade = os.path.join(path_root, FOLDER_DAILY_TRADE_PROCESSED)
    if not os.path.exists(stock_folder_daily_trade):
      os.makedirs(stock_folder_daily_trade)
    self.daily_trade_ratio_folder = stock_folder_daily_trade + '/'

    self.DR = DR(path_root, JSON_FILE_PROCESS_RECORD, CSV_SKIP_STOCK)

    print("path stock trade data", path)
    self.FLD = FLD(path=path_root)

    self.proc_id = self.DR.read_data(KEY_PROCESS, KEY_PROCESS_DAILY_TRADE_QUARTER_INDEX)
    self.stock_codes = stock_codes[self.proc_id:]

    self.data_type = data_type

  
  def trade_data_quarter(self):

    for stock_code in self.stock_codes:

      data_main = self.FLD.load_all_financial_one_stock(stock_code)
      finance_main = FILE_MAIN.format(stock_code)

      if data_main[finance_main].empty == True:

          print("no this stock", stock_code, "data")
          self.DR.write_skip_stock(stock_code)
      else:

        file_name = FILE_STOCK_DAILY_TRADE.format(stock_code)
        dates = data_main[finance_main].columns[1:self.FLD.min_column]

        daily_trade_data = self.FLD.load_financical_data([file_name])[file_name]

        # no trade data skip this stock 
        if (daily_trade_data.shape[0] == 0):
          print("no this stock", stock_code, "data")
          self.DR.write_skip_stock(stock_code)
          continue 

        daily_trade_dates = daily_trade_data.loc[:,'日期']
        trade_data_quarter = pd.DataFrame(columns=daily_trade_data.columns)

        for get_date in dates:

          date_in_daily_trade_dates = nearest_date(daily_trade_dates, get_date)
          trade_data_quarter = pd.concat([trade_data_quarter, daily_trade_data[date_in_daily_trade_dates == daily_trade_dates]])

        # trade_data_quarter.index = dates
        file_csv = self.stock_file_daily_trade_quarter.format(stock_code)
        trade_data_quarter.to_csv(file_csv, encoding='gbk')
        print("store to ", file_csv)

        self.DR.write_data(KEY_PROCESS, KEY_PROCESS_DAILY_TRADE_QUARTER_INDEX, self.proc_id)
        self.proc_id = self.proc_id + 1
  
  def price_volume_ratio(self, stock_codes, outputfile):

    scu = SCU()

    pct_columns_list = ['day1  price', 'day2', 'day3', 'day4', 'day5',\
      '5days', '10days', '20days', '60days', '100days', '200days', '400days',\
      'day1  volumn', 'day2', 'day3', 'day4', 'day5', '1vs5days_mean',\
        '5days', '10days', '20days', '200days']
    pd_total_stock = pd.DataFrame()

    for stock_code in stock_codes:

      file_name = FILE_STOCK_DAILY_TRADE.format(stock_code)

      daily_trade_data = self.FLD.load_financical_data([file_name])[file_name]

      # here need 400 trade days datas
      if daily_trade_data.shape[0] > 400:

        days = 5

        # price change
        price_data = pd.Series(daily_trade_data.loc[:, '收盘价'], dtype = np.float)

        pct_change = 0 - price_data[0 : days + 1].pct_change()[1:] * 100
        pct_change_list = list(pct_change)
        price_pct = lambda x :  (price_data[0] - price_data[x]) * 100 / price_data[x] 
        # 5 days
        pct_change_list.append( price_pct(days))
        # 10 days
        pct_change_list.append( price_pct(days * 2))
        # 20 days
        pct_change_list.append( price_pct(days * 4))
        # 60 days
        pct_change_list.append( price_pct(days * 12))
        # 100 days
        pct_change_list.append( price_pct(days * 20))
        # 200 days
        pct_change_list.append( price_pct(days * 40))
        # 400 days
        pct_change_list.append( price_pct(days * 80))

        # volumn change
        # volumn_data = pd.Series(pd.DataFrame(daily_trade_data.loc[:, '成交量']).applymap(lambda x: np.float(x)).values.squeeze())
        volumn_data = pd.Series(daily_trade_data.loc[:, '成交量'],dtype=np.float)

        volumn_change = 0 - volumn_data[0 : days + 1].pct_change()[1:] * 100
        pct_change_list = pct_change_list + list(volumn_change)
        # 1days vs 5 days
        pct_ = (volumn_data[0] - volumn_data[1 : days].mean()) * 100 / volumn_data[ 1 : days].mean()
        pct_change_list.append(pct_)
        volumn_pct = lambda x : (volumn_data[ 0 : days - 1].mean() - volumn_data[ days : 2 * days - 1].mean()) * 100 \
                / volumn_data[ days : 2 * days - 1].mean()
        # 5 days vs 5 days
        pct_ = volumn_pct(days)
        pct_change_list.append(pct_)
        # 10 days
        pct_ = volumn_pct(days * 2)
        pct_change_list.append(pct_)
        # 60 days
        pct_ = volumn_pct(days * 4)
        pct_change_list.append(pct_)
        # 200 days
        pct_ = volumn_pct(days * 40)
        pct_change_list.append(pct_)

        if self.data_type == TYPE_STOCK:
          pd_stock = pd.DataFrame(pct_change_list, columns=[scu.add_stock_sh_sz(stock_code)])
        elif self.data_type == TYPE_INDEX:
          pd_stock = pd.DataFrame(pct_change_list, columns=[stock_code])

        pd_total_stock = pd.concat([pd_total_stock, pd_stock], axis=1)
    
    pd_total_stock1 = pd.DataFrame(pd_total_stock.T.values, columns=pct_columns_list, index=pd_total_stock.columns)
    pd_total_stock1.to_csv(self.daily_trade_ratio_folder + outputfile, encoding='gbk')
    print("store to ", self.daily_trade_ratio_folder + outputfile)




