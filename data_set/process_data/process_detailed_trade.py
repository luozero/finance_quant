import pandas as pd
import numpy as np
import os

from ultility.download_record import download_record as DR
from ultility.common_func import * 
from ultility.common_def import * 
from data_set.finance_data.finance_load_store import finance_load_store as FLD
from datetime import datetime
from data_set.efinance.utils import *

class detailed_trade(object):

  def __init__(self, path = "path", path_in = 'path_in', path_out = 'path_out'):

    self.path = path
    if not os.path.exists(path_in):
      print("pls download finance data")
    self.path_in = path_in

    # path_out = os.path.join(path_out, get_today_date())
    if not os.path.exists(path_out):
      os.makedirs(path_out)
    self.path_out = path_out

  def read_excel(self, path, stock, date):
    csv_file_path = os.path.join(path, stock, str(date) + '.csv')
    if os.path.exists(csv_file_path):
      print("load file ", csv_file_path)

      # fetch data according to date align
      columns_tmp = pd.read_excel(csv_file_path, nrows = 0)
      columns = list(columns_tmp.columns)
      data = pd.read_excel(csv_file_path, usecols=columns)
      # data = pd.read_csv(csv_file_path, encoding='gbk',error_bad_lines=False)

      data = data.replace('--', 0)
      data = data.replace('_', 0)
      data = data.replace('None', 0)
      data = data.fillna(0)
    else:
      print('stock this file is not exist', csv_file_path)
      data = pd.DataFrame()
    return data

  def statistic_detailed(self, df):
    
    buy_data = df[df['性质'].isin(['买盘'])]
    sell_data = df[df['性质'].isin(['卖盘'])]

    amount_col = '成交额（元）'
    buy_amount = buy_data[amount_col]
    sell_amount = sell_data[amount_col]
    datas = [
    buy_data[buy_amount >= 100E4][amount_col].sum(),
    buy_data[(buy_amount < 100E4) & (buy_amount >= 20E4)][amount_col].sum(),
    buy_data[(buy_amount < 20E4) & (buy_amount >= 4E4)][amount_col].sum(),
    buy_data[buy_amount < 4E4][amount_col].sum(),
    sell_data[sell_amount >= 100E4][amount_col].sum(),
    sell_data[(sell_amount < 100E4) & (sell_amount >= 20E4)][amount_col].sum(),
    sell_data[(sell_amount < 200E4) & (sell_amount >= 4E4)][amount_col].sum(),
    sell_data[sell_amount < 4E4][amount_col].sum(),
    ]

    datas = [data/1E4 for data in datas]
    return datas

  def statistic_detailed_bills(self, stock_codes):

    for stock_code in stock_codes:

      detailed_files = os.listdir(os.path.join(self.path_in, stock_code))
      dates = sorted([int(detailed_file[:-4]) for detailed_file in detailed_files], reverse=True)
      stored_bill_file = os.path.join(self.path_out, stock_code, CONST_DEF.FILE_STOCK_BILL_CALC)
      if os.path.exists(stored_bill_file):
        dates = dates[:2]

      data_set = []
      for date in dates:
        df = self.read_excel(self.path_in, stock_code, date)
        if len(df) > 0:
          data_stat = self.statistic_detailed(df)
          data_set += [[date] + data_stat]

      columns = ['date', 'super_b(万)', 'big_b(万)', 'middle_b(万)', 'small_b(万)', 'super_s(万)', 'big_s(万)', 'middle_s(万)', 'small_s(万)']
      df_data_stat = pd.DataFrame(data = data_set, columns=columns)

      if os.path.exists(stored_bill_file):
        df_data_stat_hist = pd.read_csv(stored_bill_file, encoding = 'gbk')
        df_data_new = pd.concat([df_data_stat, df_data_stat_hist])
        df_data_out = df_data_new.sort_values(by = ['date'], ascending=False)
      else:
        df_data_out = df_data_stat.sort_values(by = ['date'], ascending=False)

      df_data_out.drop_duplicates(subset=['date'], inplace=True)
      print(stored_bill_file)
      df_data_out.to_csv(stored_bill_file, encoding='gbk', index=False)