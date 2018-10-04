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
    self.DR = DR(path=path,skip = 'skip_stock.csv')
  
  def stock_codes(self):
    basic_data = ts.get_stock_basics()
    stock_codes = list(basic_data.index)
    stock_codes.sort()
    return stock_codes
    
  def stock_codes_remove_no_stock_basic(self):
    stock_codes = self.stock_codes()
    skip_stocks = self.DR.read_skip_stock()
    for stock in skip_stocks:
      stock_codes.remove(stock[:-3])
    return stock_codes
if __name__ == '__main__':
  SCU = stock_codes_utility(path='../../../data/')
  stock_codes = SCU.stock_codes_remove_no_stock_basic()
  pass