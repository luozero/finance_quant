# coding: utf8
import pandas as pd
from ultility.common_def import *

def nearest_date(items, pivot):
  return min(items, key=lambda x: abs(pd.Timestamp(x) - pd.Timestamp(pivot)))

def get_stock_index_file(data_type, stock_code):
  if data_type == TYPE_STOCK:
    file_name = FILE_STOCK_DAILY_TRADE.format(stock_code)
  elif data_type == TYPE_INDEX:
    file_name = FILE_INDEX_DAILY_TRADE.format(stock_code)
  return file_name