#-*- coding:UTF-8 -*-

import pandas as pd
import numpy as np
import os

from ultility.download_record import download_record as DR
from ultility.common_func import * 
from ultility.common_def import * 
from data_set.finance_data.finance_load_store import finance_load_store as FLD
from datetime import datetime

class process_daily_trade(object):

  def __init__(self, path = "path", path_in = 'path_in', path_out = 'path_out'):

    self.path = path
    if not os.path.exists(path_in):
      print("pls download finance data")

    # path_out = os.path.join(path_out, get_today_date())
    if not os.path.exists(path_out):
      os.makedirs(path_out)
    self.path_out = path_out

    print("path stock trade data", path_in)
    self.path_in = path_in

  def nearest_date(self, items, pivot):
    return min(items.values, key=lambda x: abs(datetime.strptime(x, '%Y-%m-%d') - datetime.strptime(pivot, '%Y-%m-%d')))

  def add_index_sh_sz(self, stock):
    if int(stock[0])<3:
      stock = 'SH' + stock
    else:
      stock = 'SZ' + stock
    return stock

  def trade_data_quarter(self, stock_codes):

    dr = DR(self.path, CONST_DEF.JSON_FILE_PROCESS_RECORD, CONST_DEF.CSV_SKIP_STOCK)
    proc_id = dr.read_data(CONST_DEF.KEY_PROCESS, CONST_DEF.KEY_PROCESS_DAILY_TRADE_QUARTER_INDEX)
    stock_codes = stock_codes[proc_id:]

    for stock_code in stock_codes:

      data_main = common_func.read_csv(common_func.stock_path(self.path_in, stock_code), CONST_DEF.FILE_MAIN)

      if data_main.empty == True:

          print("no this stock", stock_code, "data")
          dr.write_skip_stock(stock_code)
      else:

        file_name = CONST_DEF.FILE_DAILY_TRADE
        daily_trade_data = common_func.read_csv(os.path.join(self.path_in, stock_code), file_name) 

        dates = data_main.columns

        # no trade data skip this stock 
        if (daily_trade_data.shape[0] == 0):
          print("no this stock", stock_code, "data")
          self.DR.write_skip_stock(stock_code)
          continue 

        daily_trade_dates = daily_trade_data.loc[:,'日期']
        trade_data_quarter = pd.DataFrame(columns=daily_trade_data.columns)

        for get_date in dates[1:-1]:
          # print(get_date)
          date_in_daily_trade_dates = self.nearest_date(daily_trade_dates, get_date)
          print(date_in_daily_trade_dates)
          trade_data_quarter = pd.concat([trade_data_quarter, daily_trade_data[date_in_daily_trade_dates == daily_trade_dates]])

        # trade_data_quarter.index = dates
        file_csv = os.path.join(common_func.stock_path(self.path_in, stock_code), CONST_DEF.FILE_DAILY_TRADE_QUARTER)
        trade_data_quarter.to_csv(file_csv, encoding='gbk', index = False)
        print("store to ", file_csv)

        dr.write_data(CONST_DEF.KEY_PROCESS, CONST_DEF.KEY_PROCESS_DAILY_TRADE_QUARTER_INDEX, proc_id)
        proc_id = proc_id + 1

  def price_volume_ratio_process1(self, daily_trade_data):

    # here need 400 trade days datas
    if daily_trade_data.shape[0] > 400:

      days = 5

      data_pct_change_one_day = lambda x: (x[0 : days].values - x[1 : days + 1].values) / x[1 : days + 1].values * 100

      # price change
      price_data = pd.Series(daily_trade_data.loc[:, '收盘价'], dtype = np.float64)
      # pct_change = 0 - price_data[0 : days + 1].pct_change()[1:] * 100
      pct_change = data_pct_change_one_day(price_data)

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
      volumn_data = pd.Series(daily_trade_data.loc[:, '成交量'],dtype=np.float64)

      # volumn_change = 0 - volumn_data[0 : days + 1].pct_change()[1:] * 100
      volumn_change = data_pct_change_one_day(volumn_data)

      pct_change_list = pct_change_list + list(volumn_change)
      # 1days vs 5 days
      pct_ = (volumn_data[0] - volumn_data[1 : days].mean()) * 100 / volumn_data[ 1 : days].mean()
      pct_change_list.append(pct_)

      volumn_pct = lambda x : (volumn_data[0 : x - 1].mean() - volumn_data[x : 2 * x - 1].mean()) * 100 \
              / volumn_data[x : 2 * x - 1].mean()
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

      pct_change_series = pd.Series(pct_change_list)

      return pct_change_series

  def index_price_volume_ratio(self, codes_names, outputfile):

    pct_columns_list = ['day1_price', 'day2', 'day3', 'day4', 'day5',\
      '1vs5days_mean', '10days', '20days', '60days', '100days', '200days', '400days',\
      'day1_volumn', 'day2', 'day3', 'day4', 'day5', '1vs5days_mean',\
        '5days', '10days', '20days', '200days']
    pct_change_pd = pd.DataFrame()

    code_names_list = []
    codes_list = []

    file_name = CONST_DEF.FILE_DAILY_TRADE

    # for stock_code in codes_names['code'] :
    for code_name in codes_names.itertuples():

      stock_code = code_name[1]
      daily_trade_data = common_func.read_csv(os.path.join(self.path_in, stock_code),  file_name)

      if daily_trade_data.shape[0] > 400:

        pct_change_series = self.price_volume_ratio_process1(daily_trade_data)
        pct_change_pd = pd.concat([pct_change_pd, pct_change_series], axis=1)

        codes_list.append("'" + code_name[1])
        
        code_name = code_name[2]
        code_names_list.append(code_name)

    pct_change_pd = pd.DataFrame(pct_change_pd.T.values, columns=pct_columns_list, index=codes_list)
    pct_change_pd = pd.concat([pd.Series(code_names_list, index=codes_list), pct_change_pd], axis=1)
    pct_change_pd.to_csv(os.path.join(self.path_out, outputfile), encoding='gbk')
    print("store to ", os.path.join(self.path_out, outputfile))