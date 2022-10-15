# coding: utf8
import os
import pandas as pd
import datetime
from ultility.common_def import *

def nearest_date(items, pivot):
  return min(items, key=lambda x: abs(pd.Timestamp(x) - pd.Timestamp(pivot)))

def get_stock_index_file(data_type, stock_code):
  if data_type == TYPE_INDEX:
    file_name = FILE_INDEX_DAILY_TRADE.format(stock_code)
  else:
    file_name = FILE_STOCK_DAILY_TRADE.format(stock_code)
  return file_name

def get_date():
  date = datetime.date.today()
  date = str(date).replace('-','')
  return date

def read_csv(path, file):
  csv_file_path = os.path.join(path, file)
  if os.path.exists(csv_file_path):
    print("load file ", csv_file_path)

    # fetch data according to date align
    columns_tmp = pd.read_csv(csv_file_path, encoding='gbk', nrows = 0)
    columns = list(columns_tmp.columns)
    data = pd.read_csv(csv_file_path, encoding='gbk', usecols=columns)
    # data = pd.read_csv(csv_file_path, encoding='gbk',error_bad_lines=False)

    data = data.replace('--', 0)
    data = data.replace('_', 0)
    data = data.replace('None', 0)
    data = data.fillna(0)
  else:
    print('stock this file is not exist', csv_file_path)
    data = pd.DataFrame()
  return data