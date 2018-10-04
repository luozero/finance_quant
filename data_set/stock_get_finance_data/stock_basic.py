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
MAX_DOWNLOAD_TIMES = 50

class stock_basic:
  def __init__(self, stock_codes=['000001'], path_root='../../../data/'):
    ts.set_token('857448afe8a838163de2ea7e3555468ca0f314a424ad47da078c9265')
    self.pro = ts.pro_api()
    path = os.path.join(path_root,'stock_basic')
    if not os.path.exists(path):
              os.makedirs(path)
    self.path = path
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
    process_index = SB.DR.read_index()
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
          SB.DR.write_skip_stock(stock)
          break
        if not stock_basic.empty:
          break
      path_csv = os.path.join(self.path,stock_store+'_basic.csv')
      stock_basic.to_csv(path_csv)
      print('this stock',stock, 'successfully downloaded')
      process_index = process_index + 1
      SB.DR.write_index(process_index)
    
  
  def get_daily_basic(self,ts_code,get_date,must_download_flag): 
    
    get_timestamp = pd.Timestamp(get_date)
    try_cnt = 0
    while True:
      str = get_timestamp.strftime('%Y%m%d')
      #stock_basic = pro.daily_basic(ts_code=ts_code, trade_date=str)
      continue_download_this_stock = True
      while continue_download_this_stock:
        continue_download_this_stock,stock_basic = self.try_download_csv(ts_code, str)

      if try_cnt<10:
        get_timestamp = get_timestamp -datetime.timedelta(days=1)
      else:
        get_timestamp = get_timestamp -datetime.timedelta(days=30)
      if must_download_flag:
        if not stock_basic.empty:
          break
      else:
        if not stock_basic.empty:
          break
        if try_cnt==MAX_DOWNLOAD_TIMES:
          break
      try_cnt = try_cnt + 1
    return stock_basic,try_cnt
  
  def get_stocks_basic(self):
    pd_skipstock = []
    for stock in self.stock_codes:
      stock_store = stock
      if int(stock)<600000:
        stock = stock + '.SZ'
      else:
        stock = stock + '.SH'
      data_main = self.FLD.load_all_financial_one_stock(stock_store)
      dates = data_main['main'].columns[1:self.FLD.min_column]
      #download_dates=[]
      pre_stock_basic,try_cnt = self.get_daily_basic(stock,dates[0],True)
      if pre_stock_basic.empty:
        pd_skipstock.append(stock)
        print('skip this stock', stock,'try_cnt',try_cnt)
        continue
      for get_date in dates:
        print('get_date',get_date)
        stock_basic,try_cnt = self.get_daily_basic(stock,get_date,False)
        print('stock is', stock, 'date is', get_date)
        if try_cnt==MAX_DOWNLOAD_TIMES:
          #download_dates.append(get_date)
          stock_basic = pre_stock_basic
        if get_date == dates[0]:
          pd_stock = stock_basic
        else:
          pd_stock = pd_stock.append(stock_basic)
        pre_stock_basic = stock_basic
        print('stock',stock,'try_cnt',try_cnt,'finished download')
      pd_stock.index = dates
      path_csv = os.path.join(self.path,stock_store+'_basic.csv')
      pd_stock.to_csv(path_csv)
      print('this stock',stock, 'successfully downloaded')
    path_csv = os.path.join(self.path,'skip_stock_basic.csv')
    pd_skipstock = pd.Series(pd_skipstock)
    pd_skipstock.to_csv(path_csv)
    
if __name__ == '__main__':
  path_root = '../../../data/'
  #stock_codes = ['000001']
  stock_codes = FD.ts_stock_codes()
  #get_dates = ['2018/6/30']
  SB = stock_basic(stock_codes, path_root)
    #SB.get_stocks_basic()
  SB.get_all_stocks_basic()
  pass