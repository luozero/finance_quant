# coding: utf8
import pandas as pd
import numpy as np
import os
import tushare as ts
from download_record import download_record as DR
'''
Created on 2018��10��4��

@author: intel
'''
class stock_codes_utility:
  def __init__(self,path='../../../data/'):
    ts.set_token('857448afe8a838163de2ea7e3555468ca0f314a424ad47da078c9265')
    self.pro = ts.pro_api()
    self.DR = DR(path=path,skip = 'skip_stock.csv')
    self.processing_DR = DR(path=path,skip = 'process_stock.csv')
  
  def stock_codes(self):
    basic_data = ts.get_stock_basics()
    stock_codes = list(basic_data.index)
    stock_codes.sort()
    return stock_codes
    
  def stock_codes_remove_no_stock_basic(self):
    if not os.path.exists(self.processing_DR.path_stock_rec):
      stock_codes = self.stock_codes()
      skip_stocks = self.DR.read_skip_stock()
      for stock in skip_stocks:
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