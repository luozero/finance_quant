#-*- coding:UTF-8 -*-
from urllib import request
import os
import tushare as ts
import pandas as pd

from stock_deeplearning.ultility.download_record import download_record as DR
from stock_deeplearning.ultility.stock_codes_utility import stock_codes_utility as SCU

from stock_deeplearning.ultility.common_def import * 

def Schedule(a,b,c):
    per = 100.0 * a * b / c
    if per > 100 :
        per = 100
    print('%.2f%%' % per)
    
def try_download_csv(path, filename, url, Schedule,stock, download_count):
  url = url.format(stock)
  filename = os.path.join(path,filename.format(stock))
  try:
    request.urlretrieve(url,filename,Schedule)
    continue_download_this_stock = 0
  except :
    print('fail to download stock ', url, 'download count ', download_count, 'one times, and try it again!!!')
    print(url)
    continue_download_this_stock = 1
  return continue_download_this_stock

def fetch_stock_finance_data(path,stock, download_count):
  #main finance
  continue_download_this_stock = try_download_csv(path, FILE_MAIN, LINK_MAIN_FINANCE, Schedule, stock, download_count)
  if continue_download_this_stock==1:
    return continue_download_this_stock

  # earning
  continue_download_this_stock = try_download_csv(path, FILE_EARNING, LINK_EARNING_CAPACITY, Schedule, stock, download_count)
  if continue_download_this_stock==1:
    return continue_download_this_stock

  # return debit
  continue_download_this_stock = try_download_csv(path, FILE_RETURN_DEBIT, LINK_RETURN_DEBIT_CAPACITY, Schedule, stock, download_count)
  if continue_download_this_stock==1:
    return continue_download_this_stock

  # growth
  continue_download_this_stock = try_download_csv(path, FILE_GROWTH, LINK_GROWTH_CAPACITY, Schedule, stock, download_count)
  if continue_download_this_stock==1:
    return continue_download_this_stock

  # operation
  continue_download_this_stock = try_download_csv(path, FILE_OPERATION, LINK_OPERATION_CAPACITY, Schedule, stock, download_count)
  if continue_download_this_stock==1:
    return continue_download_this_stock

  #abstract
  continue_download_this_stock = try_download_csv(path, FILE_ABSTRACT, LINK_ADBSTRACT_FINANCE, Schedule, stock, download_count)
  if continue_download_this_stock==1:
    return continue_download_this_stock
  #profit

  continue_download_this_stock = try_download_csv(path, FILE_PROFIT, LINK_PROFIT_FINANCE, Schedule, stock, download_count)
  if continue_download_this_stock==1:
    return continue_download_this_stock
  #cash
  continue_download_this_stock = try_download_csv(path, FILE_CASH, LINK_CASH_FINANCE, Schedule, stock, download_count)
  if continue_download_this_stock==1:
    return continue_download_this_stock
  #loans
  continue_download_this_stock = try_download_csv(path, FILE_LOANS, LINK_LOANS_FINANCE, Schedule, stock, download_count)
  if continue_download_this_stock==1:
    return continue_download_this_stock
  
  #daily trade
  if int(stock)<600000:
    url = LINK_STOCK_DAILY_TRADE_SZ
  else:
    url = LINK_STOCK_DAILY_TRADE_SH
  continue_download_this_stock = try_download_csv(path, FILE_DAILY_TRADE, url, Schedule, stock, download_count)
  if continue_download_this_stock==1:
    return continue_download_this_stock

def ts_stock_codes():
  basic_data = ts.get_stock_basics()
  stockcode = list(basic_data.index)
  stockcode.sort()
  return stockcode

def read_stock_index(download_stock_file):
  stocks_index = 0
  if os.path.exists(download_stock_file):
    try:
        his = pd.read_csv(download_stock_file)
        stocks_index = int(his.columns[1])
    except ValueError:
        print('ERR load', download_stock_file)
        return
  return stocks_index

def store_stock_index(download_stock_file, stock_index):
  his = pd.Series(stock_index)
  his.to_csv(download_stock_file)

def download_finance(path_root = '../../../data/', stock_codes = ['000001']):

  path = os.path.join(path_root, FOLDER_DATA_DOWNLOAD)
  if not os.path.exists(path):
    os.makedirs(path)

  dr = DR(path_root, FILE_JSON_PROCESS_RECORD)
  stock_index = dr.read_data(KEY_DOWNLOAD, KEY_DOWNLOAD_FINANCE_DATA_INDEX)
  stock_codes = stock_codes[stock_index:]

  DOWNLOAD_THR = 20
  for stock in (stock_codes):
    print("fetching stock", stock)
    continue_download_this_stock = 1
    download_count = 0
    while continue_download_this_stock == 1:
      continue_download_this_stock = fetch_stock_finance_data(path, stock, download_count)
      download_count = download_count + 1
      if download_count > DOWNLOAD_THR:
        break
    
    if download_count < DOWNLOAD_THR:
      # store_stock_index(download_stock_file, stock_index)
      print("download finance data successfully stock", stock)
    else:
      print("failed to download staock", stock)
    stock_index = stock_index + 1
    dr.write_data(KEY_DOWNLOAD, KEY_DOWNLOAD_FINANCE_DATA_INDEX, stock_index)

if __name__ == '__main__':
  download_finance()
  


