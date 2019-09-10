#-*- coding:UTF-8 -*-
'''
Created on 2018��10��1��

@author: intel
'''
import tushare as ts
import pandas as pd
import datetime
import os
import financial_download as FD
from financial_load_store import financial_load_store as FLD
from download_record import download_record as DR
from stock_codes_utility import stock_codes_utility as SCU
MAX_DOWNLOAD_TIMES = 50

class stock_basic:
  def __init__(self, stock_codes=['000001'], path_root='../../../data/'):
    ts.set_token('9006fc1126610a1ca69c4b1c8a91d8b5112af8d5ec1a5ba0f17a4a0b')
    self.pro = ts.pro_api()
    path = os.path.join(path_root,'stock_basic')
    if not os.path.exists(path):
              os.makedirs(path)
    #self.path = path
    self.stock_basic_path = os.path.join(path,'{}_basic.csv')
    path = os.path.join(path_root,'processed_stock_basic')
    if not os.path.exists(path):
              os.makedirs(path)
    #self.path = path
    self.stock_processed_basic_path = os.path.join(path,'{}_basic.csv')
    self.stock_codes = stock_codes
    self.FLD = FLD(path=path_root)
    self.DR = DR(path_root,'stock_basic.json')
    
  def try_download_csv(self,ts_code,date):
    stock_basic = pd.DataFrame()
    try:
      stock_basic = self.pro.daily_basic(ts_code=ts_code, trade_date=date)
      continue_download_this_stock = False
    except :
      print('fail to download stock ',ts_code, 'date',date,'one times, and try it again!!!')
      continue_download_this_stock = True
    return continue_download_this_stock, stock_basic
  
  def get_all_stocks_basic(self): 
    process_index = self.DR.read_index()
    print('process_index',process_index)
    for stock in self.stock_codes[process_index:]:
      print('stock', stock, 'is downloading','process_index',process_index)
      try_cnt = 0
      stock_store = stock
      if int(stock)<600000:
        stock = stock + '.SZ'
      else:
        stock = stock + '.SH'
      while True:
        try_cnt = try_cnt + 1
        continue_download_this_stock = True
        while continue_download_this_stock:
          continue_download_this_stock,stock_basic = self.try_download_csv(stock, '')
          print('stock', stock, 'try times', try_cnt)
        if try_cnt == MAX_DOWNLOAD_TIMES:
          print('skip this stock', stock, 'try times', try_cnt)
          self.DR.write_skip_stock(stock)
          break
        if not stock_basic.empty:
          break
      path_csv = self.stock_basic_path.format(stock_store)
      stock_basic.to_csv(path_csv)
      print('this stock',stock, 'successfully downloaded')
      process_index = process_index + 1
      self.DR.write_index(process_index)
    
  def processed_daily_basic(self,stock_basic_datas,get_date):
    try:
      get_timestamp = pd.Timestamp(get_date)
    except:
      stock_basic = stock_basic_datas.tail(1)
      return stock_basic
    stock_basic_dates = stock_basic_datas.loc[:,'trade_date']
    try_cnt = 0
    while True:
      date_str = get_timestamp.strftime('%Y%m%d')
      date_int = int(date_str)
      if date_int > stock_basic_dates.values[-1]:
        if date_int in stock_basic_dates.values:
          stock_basic = stock_basic_datas[stock_basic_dates==date_int]
          break
        else:
          get_timestamp = get_timestamp - datetime.timedelta(days=1)
      else:
        stock_basic = stock_basic_datas.tail(1)
        break
    return stock_basic
  
  def processed_stocks_basic(self):
    for stock in self.stock_codes:
      data_main = self.FLD.load_all_financial_one_stock(stock)
      dates = data_main['main'].columns[1:self.FLD.min_column]
      stock_basic_datas = self.FLD.load_all_stock_basic_one_stock([stock])
      stock_basic_datas = stock_basic_datas[stock]
      pd_stock = pd.DataFrame(columns=stock_basic_datas.columns)
      times = 0
      for get_date in dates:
        times = times + 1
        print('stock is', stock, 'date is', get_date, 'fetch time', times)
        stock_basic = self.processed_daily_basic(stock_basic_datas,get_date)
        pd_stock = pd_stock.append(stock_basic)
      pd_stock.index = dates
      path_csv = self.stock_processed_basic_path.format(stock)
      pd_stock.to_csv(path_csv)
      print('this stock',stock, 'successfully downloaded')
    
def download_all_stocks_basic(path_root = '../../../data/'):

  #stock_codes = ['000001']
  stock_codes = FD.ts_stock_codes()
  #get_dates = ['2018/6/30']
  SB = stock_basic(stock_codes, path_root)
    #SB.get_stocks_basic()
  SB.get_all_stocks_basic()
  print('downloaded successfully')

def processed_all_stocks_basic(path_root = '../../../data/'):

  scu = SCU(path=path_root)
  
  stock_codes = scu.stock_codes_remove_no_stock_basic()
  #stock_codes = ['001965']
  #get_dates = ['2018/6/30']
  SB = stock_basic(stock_codes, path_root)
    #SB.get_stocks_basic()
  SB.processed_stocks_basic()
  print('processed successfully')

if __name__ == '__main__':
  download_all_stocks_basic()
  processed_all_stocks_basic()
  pass