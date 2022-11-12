# coding: utf8
import os
import json
import pandas as pd
import datetime
from ultility.common_def import *
import efinance as ef

class common_func:
  def stock_path(path, stock):
    path = os.path.join(path, stock)
    if not os.path.exists(path):
      os.makedirs(path)
    return path

  def get_today_date():
    date = datetime.date.today()
    date = str(date).replace('-','')
    return date

  def read_config(filename):
    with open(filename, 'r') as f:
      conf = json.load(f)
    return conf

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

  def add_stock_sh_sz_bj(stock):
    if int(stock)<600000:
      stock = 'SZ' + str(stock)
    elif int(stock) < 800000:
      stock = 'SH' + str(stock)
    else:
      stock = 'BJ' + str(stock)
    return stock
