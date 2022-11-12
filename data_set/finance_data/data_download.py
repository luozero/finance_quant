#-*- coding:UTF-8 -*-
from urllib import request
import os
import tushare as ts
import pandas as pd
import datetime
from retry import retry

from ultility.download_record import download_record as DR
from ultility.common_def import * 
from ultility.common_func import * 

DELAY = 50
TRY_TIMES = 50

class data_download:
  def __init__(self, path = 'path', path_data='../../../data/', stock_codes=['000001'], type_data = CONST_DEF.TYPE_FINANCE_STOCK):

    self.path = path
    if not os.path.exists(self.path):
      os.makedirs(self.path)

    self.path_data = path_data
    if not os.path.exists(self.path_data):
      os.makedirs(self.path_data)
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

    filename = os.path.join(common_func.stock_path(self.path_data, stock), filename)
    stock_change = stock
    # download
    try:
      url = url.format(stock_change, self.date)
      print(url)
      request.urlretrieve(url, filename, self.Schedule)
      print("stored file: ", filename)
    except:
      print('skip this stok: ', stock)

  def change_stock_code(self, stock):
    a = stock[0]
    if self.type_data.find('index') > -1:
      if int(a) >= 3:
        stock_change = '1' + stock
      else:
        stock_change = '0' + stock
    else:
      if int(a) >= 6:
        stock_change = '0' + stock
      else:
        stock_change = '1' + stock
    return stock_change

  @retry(tries=-1, delay=100) 
  def try_download_detailed_csv(self, url, date, stock):

    stock_change = self.change_stock_code(stock)
    # download
    try:
      filename = os.path.join(common_func.stock_path(self.path_data, stock), date + '.csv')
      url = url.format(date, stock_change)
      print(url)
      request.urlretrieve(url, filename, self.Schedule)
      print("stored file: ", filename)
    except:
      print('skip this stok: ', stock)

  def download_detailed(self, date, stock):
    url = 'http://quotes.money.163.com/cjmx/' + date[:4] + '/{}/{}.xls'
    self.try_download_detailed_csv(url, date, stock)

  @retry(tries=-1, delay=DELAY)
  def try_download_trade_csv(self, filename, url, stock):

    stock_change = self.change_stock_code(stock)

    # download
    try:
      filename = os.path.join(common_func.stock_path(self.path_data, stock), filename)
      url = url.format(stock_change, self.date)
      print(url)
      request.urlretrieve(url, filename, self.Schedule)
      print("stored file: ", filename)
    except:
      print('skip this stok: ', stock)
    
  def download_daily_trade(self, stock):
    #daily trade
    file_name = CONST_DEF.FILE_DAILY_TRADE
    if self.type_data == CONST_DEF.TYPE_INDEX:
      link = CONST_DEF.LINK_INDEX_DAILY_TRADE
    else:
      link = CONST_DEF.LINK_STOCK_DAILY_TRADE
    self.try_download_trade_csv(file_name, link, stock)

  def download_finance_data(self, stock):
    #main finance
    self.try_download_csv(CONST_DEF.FILE_MAIN, CONST_DEF.LINK_MAIN_FINANCE, stock)
    # earning
    self.try_download_csv(CONST_DEF.FILE_EARNING, CONST_DEF.LINK_EARNING_CAPACITY, stock)
    # return debit
    self.try_download_csv(CONST_DEF.FILE_RETURN_DEBIT, CONST_DEF.LINK_RETURN_DEBIT_CAPACITY, stock)
    # growth
    self.try_download_csv(CONST_DEF.FILE_GROWTH, CONST_DEF.LINK_GROWTH_CAPACITY, stock)
    # operation
    self.try_download_csv(CONST_DEF.FILE_OPERATION, CONST_DEF.LINK_OPERATION_CAPACITY, stock)
    #abstract
    self.try_download_csv(CONST_DEF.FILE_ABSTRACT, CONST_DEF.LINK_ADBSTRACT_FINANCE, stock)
    #profit
    self.try_download_csv(CONST_DEF.FILE_PROFIT, CONST_DEF.LINK_PROFIT_FINANCE, stock)
    #cash
    self.try_download_csv(CONST_DEF.FILE_CASH, CONST_DEF.LINK_CASH_FINANCE, stock)
    #loans
    self.try_download_csv(CONST_DEF.FILE_LOANS, CONST_DEF.LINK_LOANS_FINANCE, stock)
    # stock daily trade
    self.download_daily_trade(stock)

  def download_data(self, data_type = True, trade_dates = ['20221108']):
    if data_type == CONST_DEF.TYPE_FINANCE_STOCK:
      dr = DR(self.path, CONST_DEF.JSON_FILE_PROCESS_RECORD)
      stock_index = dr.read_data(CONST_DEF.KEY_DOWNLOAD, CONST_DEF.KEY_DOWNLOAD_FINANCE_DATA_INDEX)
    else:
      stock_index = 0
    stock_codes = self.stock_codes[stock_index:]

    for stock in (stock_codes):
      print("fetching code: ", stock)
      if data_type == CONST_DEF.TYPE_FINANCE_STOCK:
        self.download_finance_data(stock)
        dr.write_data(CONST_DEF.KEY_DOWNLOAD, CONST_DEF.KEY_DOWNLOAD_FINANCE_DATA_INDEX, stock_index)
      elif data_type == CONST_DEF.TYPE_STOCK or data_type == CONST_DEF.TYPE_INDEX:
        self.download_daily_trade(stock)
      elif data_type == CONST_DEF.TYPE_DETAILED_STOCK or data_type == CONST_DEF.TYPE_DETAILED_INDEX:
          for trade_date in trade_dates:
            print(trade_date)
            self.download_detailed(trade_date.replace('-', ''), stock)
      else:
        print('do not support this download type', data_type)

      if data_type == CONST_DEF.TYPE_FINANCE_STOCK:
        stock_index = stock_index + 1

if __name__ == '__main__':
  download_finance()
  


