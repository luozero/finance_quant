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

class stock_basic:
  def __init__(self, stock_codes=['000001'], dates=['2018-03-31'], path_root='../../../data/'):
    ts.set_token('857448afe8a838163de2ea7e3555468ca0f314a424ad47da078c9265')
    path = os.path.join(path_root,'stock_basic')
    if not os.path.exists(path):
              os.makedirs(path)
    self.path = path
    self.stock_codes = stock_codes
    self.get_dates = dates
    
  def try_download_csv(self,ts_code,date):
    stock_basic = pd.DataFrame()
    try:
      pro = ts.pro_api()
      stock_basic = pro.daily_basic(ts_code=ts_code, trade_date=date)
      continue_download_this_stock = False
    except :
      print('fail to download stock ',ts_code, 'date',date,'one times, and try it again!!!')
      continue_download_this_stock = True
    return continue_download_this_stock, stock_basic
  
  def get_daily_basic(self,ts_code,get_date): 
    get_timestamp = pd.Timestamp(get_date)
    try_cnt = 0
    while True:
      str = get_timestamp.strftime('%Y%m%d')
      #stock_basic = pro.daily_basic(ts_code=ts_code, trade_date=str)
      continue_download_this_stock = True
      while continue_download_this_stock:
        continue_download_this_stock,stock_basic = self.try_download_csv(ts_code, str)
      if stock_basic.empty:
        get_timestamp = get_timestamp +datetime.timedelta(days=1)
      else:
        break
      try_cnt = try_cnt + 1
      if try_cnt==10:
        break
    return stock_basic,try_cnt
  
  def get_stocks_basic(self):
    for stock in self.stock_codes:
      print('stock is', stock)
      stock_store = stock
      if int(stock)<600000:
        stock = stock + '.SZ'
      else:
        stock = stock + '.SH'
      download_dates=[]
      for get_date in self.get_dates:
        stock_basic,try_cnt = self.get_daily_basic(stock,get_date)
        if try_cnt!=10:
          download_dates.append(get_date)
        if get_date == get_dates[0]:
          pd_stock = stock_basic
        else:
          pd_stock = pd_stock.append(stock_basic)
        print('stock',stock,'try_cnt',try_cnt,'finished download')
      pd_stock.index = download_dates
      path_csv = os.path.join(self.path,stock_store+'_basic.csv')
      pd_stock.to_csv(path_csv)
  
  def load_stock_basic(self):
    data_basic = {}
    for stock in self.stock_codes:
      path_csv = os.path.join(self.path,stock+'_basic.csv')
      pd_basic = pd.read_csv(path_csv,index_col=0)
      data_basic[stock] = pd_basic
    self.stock_basic = data_basic
  
  def get_data_stock_basic(self,stock,date,factor):
    data = self.stock_basic[stock]
    
if __name__ == '__main__':
  path_root = '../../../data/'
  stock_codes = ['000155']
  #stock_codes = FD.ts_stock_codes()
  get_dates = ['2018-06-30', '2018-03-31', '2017-12-31', '2017-09-30', '2017-06-30']
  #stock_basic = get_daily_basic('000001.SZ','2018-06-30')
  
  SB = stock_basic(stock_codes, get_dates, path_root)
  SB.get_stocks_basic()
  pass