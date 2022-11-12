# coding: utf8
import os
import pandas as pd
import tushare as ts
from ultility.download_record import download_record as DR
from ultility.common_def import *
from data_set.efinance.utils import *
KECHUANG_CODE = 688000
'''
Created on 2018��10��4��

@author: intel
'''
class stock_codes_utility:
  def __init__(self,path='../../../data/', type_data = CONST_DEF.TYPE_STOCK):

    self.DR = DR(path=path, record = 'rec.json', skip = CONST_DEF.CSV_SKIP_STOCK)
    self.processing_DR = DR(path=path, record = 'rec.json', skip = CONST_DEF.CSV_SKIP_STOCK)

    if type_data.find('index') > -1:
      table = pd.read_csv('./table/index_codes.csv', encoding='gbk')
    else:
      table = pd.read_csv('./table/stock_codes.csv', encoding='gbk')
    table_tmp = table.loc[:, ['name','code']]
    table_tmp['code'] = table_tmp['code'].apply(lambda x: x[2:])
    self.table = table_tmp
    self.type_data = type_data
    
  def stock_codes_from_table(self):
    codes = sorted(self.table.loc[:,'code'].values.squeeze())
    return codes

  def stock_codes_names_from_table(self):
    table = self.table.loc[:, ['code', 'name']]
    codes = table.sort_values(by = ['code'])
    return codes

  def block_codes_names_from_eastmoney(self, block = 'indurstry'):
    return ef_utils.get_block_codes_names(block)

  def block_codes_from_eastmoney(self, block = 'indurstry'):
    return ef_utils.get_block_codes_names(block).loc[:,'stock_code'].values.squeeze()

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