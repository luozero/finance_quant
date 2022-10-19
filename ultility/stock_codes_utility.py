# coding: utf8
import os
import pandas as pd
import tushare as ts
from ultility.download_record import download_record as DR
from ultility.common_def import *
KECHUANG_CODE = 688000
'''
Created on 2018��10��4��

@author: intel
'''
class stock_codes_utility:
  def __init__(self,path='../../../data/', type_data = TYPE_STOCK):
    ts.set_token('ddd82cf225ed602f13bfcde56ef943643d79634125e3449dc9dce182')
    self.pro = ts.pro_api()
    self.DR = DR(path=path, record = 'rec.json', skip = CSV_SKIP_STOCK)
    self.processing_DR = DR(path=path, record = 'rec.json', skip = CSV_SKIP_STOCK)

    if type_data == TYPE_INDEX:
      self.table = pd.read_csv('./table/index_codes.csv', encoding='gbk')
    else:
      self.table = pd.read_csv('./table/stock_codes.csv', encoding='gbk')
    self.type_data = type_data
  
  def stock_codes(self):
    # basic_data = ts.get_stock_basics()
    basic_data = self.pro.query('stock_basic', exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
    # print(basic_data['ts_code'])
    stock_codes_tmp = self.rm_allstock_sh_sz(list(basic_data['ts_code']))

    stock_codes = []
    for i, v in enumerate(stock_codes_tmp):
      if int(v) < KECHUANG_CODE:
        stock_codes.append(v)

    stock_codes.sort()
    print(stock_codes)
    return stock_codes
  
  def stock_codes_from_table(self, type):
    codes = sorted(self.table.loc[:,'code'].apply(lambda x: x[2:]).values.squeeze())
    return codes

  def stock_codes_get_name(self, code):
    data = self.table
    return data[data['code'].isin([code])]['name'].values[0]

  def skip_stock_codes(self, stock_codes):

    if os.path.exists(self.DR.path_stock_rec):
      skip_stocks = self.DR.read_skip_stock()
      if False == skip_stocks.empty:
        for stock in skip_stocks:
          if stock in stock_codes:
            stock_codes.remove(stock)
    return stock_codes
    
  def stock_codes_remove_no_stock_basic(self):
    if not os.path.exists(self.processing_DR.path_stock_rec):
      stock_codes = self.stock_codes()
      skip_stocks = self.DR.read_skip_stock()
      if False == skip_stocks.empty:
        for stock in skip_stocks:
          if stock[:-3] in stock_codes:
            stock_codes.remove(stock[:-3])
      stock_codes_store = self.add_allstock_sh_sz(stock_codes)
      self.processing_DR.write_stock(stock_codes_store)
    else:
      stock_codes = self.processing_DR.read_stock()
      stock_codes = self.rm_allstock_sh_sz(stock_codes)
    return stock_codes
  
  def add_stock_sh_sz(self,stock):
    if int(stock)<600000:
      stock = stock + '.SZ'
    else:
      stock = stock + '.SH'
    return stock
  
  def rm_stock_sh_sz(self,stock):
    stock = stock[:-3]
    return stock
  def add_allstock_sh_sz(self,stocks):
    stock_add_shsz = []
    for stock in stocks:
      stock_add_shsz.append(self.add_stock_sh_sz(stock))
    return stock_add_shsz
  def rm_allstock_sh_sz(self,stocks):
    stock_rm_shsz = []
    for stock in stocks:
      stock_rm_shsz.append(self.rm_stock_sh_sz(stock))
    return stock_rm_shsz
  
  def add_stock_xshg_xshe(self,stock):
    if int(stock)<600000:
      stock = stock + '.XSHE'
    else:
      stock = stock + '.XSHG'
    return stock
  
  def rm_stock_xshg_xshe(self,stock):
    stock = stock[:-5]
    return stock
  def add_allstock_xshg_xshe(self,stocks):
    add_stock_xshg_xshe = []
    for stock in stocks:
      add_stock_xshg_xshe.append(self.add_stock_xshg_xshe(stock))
    return add_stock_xshg_xshe
  def rm_allstock_xshg_xshe(self,stocks):
    rm_stock_xshg_xshe = []
    for stock in stocks:
      rm_stock_xshg_xshe.append(self.rm_stock_xshg_xshe(stock))
    return rm_stock_xshg_xshe
  
if __name__ == '__main__':
  SCU = stock_codes_utility(path='../../../data/')
  stock_codes = SCU.stock_codes_remove_no_stock_basic()
  pass