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

  def get_data_common_index_block(self, codes,):

    for code in codes:
      print("download code", code)
      data = ef.stock.get_quote_history(code)
      data = data.sort_values(by = ['日期'], ascending=False)
      file = os.path.join(stock_path(self.path, code), FILE_INDEX_DAILY_TRADE)
      data.to_csv(file, encoding='gbk', index = False)

  def get_index_block_data(self, indexs = ['sh', 'sz', 'sh_sz', 'cn'], blocks = ['indurstry', 'concept', 'province']):
      
    for block in blocks:
      code_names = self.push2_98_getter.get_block_codes(block)
      self.get_data_common_index_block(code_names.loc[:, 'code'].values)

    for index in indexs:
      code_names = self.push2_98_getter.get_index_codes(index)
      self.get_data_common_index_block(code_names.loc[:, 'code'].values)

  def get_stock_north(self):

    north_stock_status = self.datacenter.get_north_stock_status()
    stock_codes = north_stock_status['stock_code'].apply(lambda x: x[:-3]).values
    for stock_code in stock_codes:

      df = self.datacenter.get_north_stock_daily_trade(stock_code)

      filename = os.path.join(stock_path(self.path, stock_code), FILE_TRADE_NORTH)
      if os.path.exists(filename):
        df_old = pd.read_csv(filename, encoding='gbk')
        df = pd.concat([df, df_old], axis = 0)
      df = df.drop_duplicates()

      df.to_csv(filename, encoding = 'gbk', index = False)
      print('stored north', filename)

  def update_north_index_data(self, df):

    stock_codes = df['stock_code']
    for stock_code in stock_codes:
      # print("process: ", stock_code)
      data_one = df[df['stock_code'].isin([stock_code])]
      file_out = os.path.join(stock_path(self.path, stock_code), FILE_INDEX_NORTH_DAILY_TRADE)
      if os.path.exists(file_out):
        data_file = pd.read_csv(file_out, encoding='gbk')
        data_update = pd.concat([data_one, data_file])
        data_update = data_update.sort_values(by = ['date'], ascending=False)
        data_update = data_update.drop_duplicates()
        data_update.to_csv(file_out, encoding = 'gbk', index = False)
      else:
        data_one.to_csv(file_out, encoding = 'gbk', index = False)
  
  def get_stock_north_index(self):

    temp_path = os.path.join(self.path, 'north_index_temp')
    if not os.path.exists(temp_path):
      os.makedirs(temp_path)
      date_series = pd.date_range(start = '2020-01-01', end = str(datetime.date.today()))
      for date in date_series:
        date_str = str(date)[0:10]
        df = self.datacenter.get_north_stock_index(date_str)
        print('download north index successfully: ', date_str)
        if len(df) > 0:
          df.to_csv(os.path.join(temp_path, date_str + '.csv'), encoding = 'gbk', index = False)

      files = os.listdir(temp_path)
      for file in files:
        print('process file: ', file)
        df = pd.read_csv(os.path.join(temp_path, file), encoding = 'gbk')
        self.update_north_index_data(df)
    else:
      date_str = str(datetime.date.today())[0:10]
      df = self.datacenter.get_north_stock_index(date_str)
      if (len(df) > 0):
        print('download north index successfully: ', date_str)
        self.update_north_index_data(df)

      # files = os.listdir(temp_path)
      # for file in files:
      #   print('process file: ', file)
      #   df = pd.read_csv(os.path.join(temp_path, file), encoding = 'gbk')
      #   self.update_north_index_data(df)

  def get_stock_margin_short(self):

    margin_short_stock_status = self.datacenter.get_margin_short_stock_status()
    stock_codes = margin_short_stock_status['stock_code'].apply(lambda x: x[:-3]).values
    for stock_code in stock_codes:
      df = self.datacenter.get_margin_short_stock(stock_code)
      filename = os.path.join(stock_path(self.path, stock_code), FILE_TRADE_MAEGIN_SHORT)
      df.to_csv(filename, encoding = 'gbk', index = False)
      print('stored north', filename)