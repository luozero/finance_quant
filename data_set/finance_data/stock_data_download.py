#-*- coding:UTF-8 -*-
from urllib import request
import os
import tushare as ts
import pandas as pd
import datetime

from stock_deeplearning.ultility.download_record import download_record as DR
from stock_deeplearning.ultility.stock_codes_utility import stock_codes_utility as SCU
from stock_deeplearning.ultility.common_def import * 


class stock_data_download:
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
      
  def try_download_csv(self, filename, url, stock, download_count):

    url = url.format(stock, self.date)

    filename = os.path.join(self.path,filename.format(stock))
    try:
      request.urlretrieve(url,filename, self.Schedule)
      continue_download_this_stock = 0
    except :
      print('fail to download stock ', url, 'download count ', download_count, 'one times, and try it again!!!')
      print(url)
      continue_download_this_stock = 1
    return continue_download_this_stock

  def download_daily_trade(self, stock, download_count):
    #daily trade
    if int(stock)<600000:
      url = LINK_STOCK_DAILY_TRADE_SZ
    else:
      url = LINK_STOCK_DAILY_TRADE_SH
    continue_download_this_stock = self.try_download_csv(FILE_DAILY_TRADE, url, stock, download_count)
    if continue_download_this_stock==1:
      return continue_download_this_stock

  def download_finance_data(self, stock, download_count):
    #main finance
    continue_download_this_stock = self.try_download_csv(FILE_MAIN, LINK_MAIN_FINANCE, stock, download_count)
    if continue_download_this_stock==1:
      return continue_download_this_stock

    # earning
    continue_download_this_stock = self.try_download_csv(FILE_EARNING, LINK_EARNING_CAPACITY, stock, download_count)
    if continue_download_this_stock==1:
      return continue_download_this_stock

    # return debit
    continue_download_this_stock = self.try_download_csv(FILE_RETURN_DEBIT, LINK_RETURN_DEBIT_CAPACITY, stock, download_count)
    if continue_download_this_stock==1:
      return continue_download_this_stock

    # growth
    continue_download_this_stock = self.try_download_csv(FILE_GROWTH, LINK_GROWTH_CAPACITY, stock, download_count)
    if continue_download_this_stock==1:
      return continue_download_this_stock

    # operation
    continue_download_this_stock = self.try_download_csv(FILE_OPERATION, LINK_OPERATION_CAPACITY, stock, download_count)
    if continue_download_this_stock==1:
      return continue_download_this_stock

    #abstract
    continue_download_this_stock = self.try_download_csv(FILE_ABSTRACT, LINK_ADBSTRACT_FINANCE, stock, download_count)
    if continue_download_this_stock==1:
      return continue_download_this_stock
    #profit

    continue_download_this_stock = self.try_download_csv(FILE_PROFIT, LINK_PROFIT_FINANCE, stock, download_count)
    if continue_download_this_stock==1:
      return continue_download_this_stock
    #cash
    continue_download_this_stock = self.try_download_csv(FILE_CASH, LINK_CASH_FINANCE, stock, download_count)
    if continue_download_this_stock==1:
      return continue_download_this_stock
    #loans
    continue_download_this_stock = self.try_download_csv(FILE_LOANS, LINK_LOANS_FINANCE, stock, download_count)
    if continue_download_this_stock==1:
      return continue_download_this_stock

    continue_download_this_stock = self.download_daily_trade(stock, download_count)
    return continue_download_this_stock

  def download_finance(self, download_all = True):

    if download_all:
      dr = DR(self.path, JSON_FILE_PROCESS_RECORD)
      stock_index = dr.read_data(KEY_DOWNLOAD, KEY_DOWNLOAD_FINANCE_DATA_INDEX)
    else:
      stock_index = 0
    stock_codes = self.stock_codes[stock_index:]

    DOWNLOAD_THR = 20
    for stock in (stock_codes):

      print("fetching stock", stock)
      continue_download_this_stock = 1
      download_count = 0
      while continue_download_this_stock == 1:
        if download_all:
          continue_download_this_stock = self.download_finance_data(stock, download_count)
        else:
          continue_download_this_stock = self.download_daily_trade(stock, download_count)
        download_count = download_count + 1
        if download_count > DOWNLOAD_THR:
          break
      
      if download_count < DOWNLOAD_THR:
        print("download daily trade data successfully stock ", stock)
      else:
        print("failed to download daily trade data stock ", stock)

      if download_all:
        stock_index = stock_index + 1
        dr.write_data(KEY_DOWNLOAD, KEY_DOWNLOAD_FINANCE_DATA_INDEX, stock_index)

if __name__ == '__main__':
  download_finance()
  


