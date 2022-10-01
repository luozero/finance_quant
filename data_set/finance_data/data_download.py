#-*- coding:UTF-8 -*-
from urllib import request
import os
import tushare as ts
import pandas as pd
import datetime
from retry import retry

from ultility.download_record import download_record as DR
from ultility.common_def import * 


DOWNLOAD_THR = 20
try_index = 0

class data_download:
  def __init__(self, path='../../../data/', stock_codes=['000001']):

    self.path = os.path.join(path, FOLDER_DATA_DOWNLOAD)
    if not os.path.exists(self.path):
      os.makedirs(self.path)
    date = datetime.date.today()
    
    self.date = str(date).replace('-','')

    self.stock_codes = stock_codes

  def Schedule(self, a,b,c):
      per = 100.0 * a * b / c
      if per > 100 :
          per = 100
      print('%.2f%%' % per)
  
  def file_name(self, filename, stock):
    return os.path.join(self.path,filename.format(stock))

  @retry(DOWNLOAD_THR) 
  def try_download_csv(self, filename, url, stock):

    url = url.format(stock, self.date)

    request.urlretrieve(url, filename, self.Schedule)
    
    # try_index = try_index + 1
    # if try_index > DOWNLOAD_THR:
    #   print('fail to download stock ', url, 'try_index ', try_index)

  def download_stock_daily_trade(self, stock):
    #daily trade
    if int(stock)<600000:
      stock_change = '1' + stock
    else:
      stock_change = '0' + stock
    self.try_download_csv(self.file_name(FILE_STOCK_DAILY_TRADE, stock), LINK_STOCK_DAILY_TRADE, stock_change)

  def download_index_daily_trade(self, stock):
    #daily trade
    a = stock[2]
    if int(a) >= 3:
      stock_change = '1' + stock[2:]
    else:
      stock_change = '0' + stock[2:]
    self.try_download_csv(self.file_name(FILE_STOCK_DAILY_TRADE, stock), LINK_INDEX_DAILY_TRADE, stock_change)

  def download_finance_data(self, stock):
    #main finance
    self.try_download_csv(self.file_name(FILE_MAIN, stock), LINK_MAIN_FINANCE, stock)
    # earning
    self.try_download_csv(self.file_name(FILE_EARNING, stock), LINK_EARNING_CAPACITY, stock)
    # return debit
    self.try_download_csv(self.file_name(FILE_RETURN_DEBIT, stock), LINK_RETURN_DEBIT_CAPACITY, stock)
    # growth
    self.try_download_csv(self.file_name(FILE_GROWTH, stock), LINK_GROWTH_CAPACITY, stock)
    # operation
    self.try_download_csv(self.file_name(FILE_OPERATION, stock), LINK_OPERATION_CAPACITY, stock)
    #abstract
    self.try_download_csv(self.file_name(FILE_ABSTRACT, stock), LINK_ADBSTRACT_FINANCE, stock)
    #profit
    self.try_download_csv(self.file_name(FILE_PROFIT, stock), LINK_PROFIT_FINANCE, stock)
    #cash
    self.try_download_csv(self.file_name(FILE_CASH, stock), LINK_CASH_FINANCE, stock)
    #loans
    self.try_download_csv(self.file_name(FILE_LOANS, stock), LINK_LOANS_FINANCE, stock)
    # stock daily trade
    self.download_stock_daily_trade(stock)


  def download_data(self, download_type = True):

    if download_type == TYPE_FINANCE_STOCK:
      dr = DR(self.path, JSON_FILE_PROCESS_RECORD)
      stock_index = dr.read_data(KEY_DOWNLOAD, KEY_DOWNLOAD_FINANCE_DATA_INDEX)
    else:
      stock_index = 0
    stock_codes = self.stock_codes[stock_index:]

    for stock in (stock_codes):

      print("fetching code: ", stock)

      if download_type == TYPE_FINANCE_STOCK:
        self.download_finance_data(stock)
        dr.write_data(KEY_DOWNLOAD, KEY_DOWNLOAD_FINANCE_DATA_INDEX, stock_index)
      elif download_type == TYPE_STOCK:
        self.download_stock_daily_trade(stock)
      elif download_type == TYPE_INDEX:
        self.download_index_daily_trade(stock)
      else:
        print('do not support this download type', download_type)

      if download_type == TYPE_FINANCE_STOCK:
        stock_index = stock_index + 1

if __name__ == '__main__':
  download_finance()
  


