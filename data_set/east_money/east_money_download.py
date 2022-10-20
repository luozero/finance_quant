import os
import sys
import datetime

from ultility.common_func import *
from ultility.common_def import *
import efinance as ef

class east_money_download:
  def __init__(self, path):
    
    self.path = path
    if not os.path.exists(path):
      os.makedirs(path)

    self.push2_98_getter = ef.stock.push2_98_getter.push2_98()
    self.datacenter = ef.stock.datacenter()

  def get_data_common(self, codes, path):

    if not os.path.exists(path):
      os.makedirs(path)
    for code in codes:
      print("download code", code)
      data = ef.stock.get_quote_history(code)
      file = os.path.join(path, code + '.csv')
      data.to_csv(file, encoding='gbk')
     
    
  def get_index_block_data(self, indexs = ['sh', 'sz', 'sh_sz', 'cn'], blocks = ['indurstry', 'concept', 'province']):
      
    for block in blocks:
      code_names = self.push2_98_getter.get_block_codes(block)
      self.get_data_common(code_names.loc[:, 'code'].values, os.path.join(self.path, block))

    for index in indexs:
      code_names = self.push2_98_getter.get_index_codes(index)
      self.get_data_common(code_names.loc[:, 'code'].values, os.path.join(self.path, index))

  def get_stock_north(self):

    north_stock_status = self.datacenter.get_north_stock_status()
    stock_codes = north_stock_status['stock_code'].apply(lambda x: x[:-3]).values
    for stock_code in stock_codes:
      df = self.datacenter.get_north_stock_daily_trade(stock_code)
      filename = os.path.join(stock_path(self.path, stock_code), FILE_TRADE_NORTH)
      df.to_csv(filename, encoding = 'gbk', index = False)
      print('stored north', filename)

  def get_stock_margin_short(self):

    margin_short_stock_status = self.datacenter.get_margin_short_stock_status()
    stock_codes = margin_short_stock_status['stock_code'].apply(lambda x: x[:-3]).values
    for stock_code in stock_codes:
      df = self.datacenter.get_margin_short_stock(stock_code)
      filename = os.path.join(stock_path(self.path, stock_code), FILE_TRADE_MAEGIN_SHORT)
      df.to_csv(filename, encoding = 'gbk', index = False)
      print('stored north', filename)