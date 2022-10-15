#-*- coding:UTF-8 -*-
from urllib import request
import os
import tushare as ts
import pandas as pd
import datetime
from retry import retry

from ultility.download_record import download_record as DR
from ultility.common_def import * 

DELAY = 50

class data_download:
  def __init__(self, path='../../../data/', stock_codes=['000001'], type_data = TYPE_FINANCE_STOCK):

    self.path = path
    if not os.path.exists(self.path):
      os.makedirs(self.path)
    date = datetime.date.today()
    
    self.date = str(date).replace('-','')

    self.stock_codes = stock_codes
    self.type_data = type_data

  def Schedule(self, a,b,c):
      per = 100.0 * a * b / c
      if per > 100 :
          per = 100
      print('%.2f%%' % per)

  @retry(tries=-1, delay=DELAY) 
  def try_download_csv(self, filename, url, stock):
    filename = os.path.join(self.path, filename.format(stock))
    stock_change = stock[2:]
    # download
    try:
      url = url.format(stock_change, self.date)
      request.urlretrieve(url, filename, self.Schedule)
    except:
      print('skip this stok: ', stock)

  @retry(tries=-1, delay=DELAY)
  def try_download_trade_csv(self, filename, url, stock):
    filename = os.path.join(self.path, filename.format(stock))
    a = stock[2]
    if self.type_data == TYPE_INDEX:
      if int(a) >= 3:
        stock_change = '1' + stock[2:]
      else:
        stock_change = '0' + stock[2:]
    else:
      if int(a) >= 6:
        stock_change = '0' + stock[2:]
      else:
        stock_change = '1' + stock[2:]
    # download
    try:
      url = url.format(stock_change, self.date)
      print(url)
      request.urlretrieve(url, filename, self.Schedule)
    except:
      print('skip this stok: ', stock)
    
  def download_daily_trade(self, stock):
    #daily trade
    if self.type_data == TYPE_INDEX:
      file_name = FILE_INDEX_DAILY_TRADE
      link = LINK_INDEX_DAILY_TRADE
    else:
      file_name = FILE_STOCK_DAILY_TRADE
      link = LINK_STOCK_DAILY_TRADE
    self.try_download_trade_csv(file_name, link, stock)

  def download_finance_data(self, stock):
    #main finance
    self.try_download_csv(FILE_MAIN, LINK_MAIN_FINANCE, stock)
    # earning
    self.try_download_csv(FILE_EARNING, LINK_EARNING_CAPACITY, stock)
    # return debit
    self.try_download_csv(FILE_RETURN_DEBIT, LINK_RETURN_DEBIT_CAPACITY, stock)
    # growth
    self.try_download_csv(FILE_GROWTH, LINK_GROWTH_CAPACITY, stock)
    # operation
    self.try_download_csv(FILE_OPERATION, LINK_OPERATION_CAPACITY, stock)
    #abstract
    self.try_download_csv(FILE_ABSTRACT, LINK_ADBSTRACT_FINANCE, stock)
    #profit
    self.try_download_csv(FILE_PROFIT, LINK_PROFIT_FINANCE, stock)
    #cash
    self.try_download_csv(FILE_CASH, LINK_CASH_FINANCE, stock)
    #loans
    self.try_download_csv(FILE_LOANS, LINK_LOANS_FINANCE, stock)
    # stock daily trade
    self.download_daily_trade(stock)

  def download_data(self, data_type = True):
    if data_type == TYPE_FINANCE_STOCK:
      dr = DR(self.path, '../' + JSON_FILE_PROCESS_RECORD)
      stock_index = dr.read_data(KEY_DOWNLOAD, KEY_DOWNLOAD_FINANCE_DATA_INDEX)
    else:
      stock_index = 0
    stock_codes = self.stock_codes[stock_index:]

    for stock in (stock_codes):
      print("fetching code: ", stock)
      if data_type == TYPE_FINANCE_STOCK:
        self.download_finance_data(stock)
        dr.write_data(KEY_DOWNLOAD, KEY_DOWNLOAD_FINANCE_DATA_INDEX, stock_index)
      elif data_type == TYPE_STOCK or data_type == TYPE_INDEX:
        self.download_daily_trade(stock)
      else:
        print('do not support this download type', data_type)

      if data_type == TYPE_FINANCE_STOCK:
        stock_index = stock_index + 1

if __name__ == '__main__':
  download_finance()
  


