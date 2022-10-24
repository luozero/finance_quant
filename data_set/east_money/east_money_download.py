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
      self.get_data_common_index_block(code_names.loc[:, 'stock_code'].values)

    for index in indexs:
      code_names = self.push2_98_getter.get_index_codes(index)
      self.get_data_common_index_block(code_names.loc[:, 'stock_code'].values)

  def combine_two_data(self, stock_code, file_name, df):

    filename = os.path.join(stock_path(self.path, stock_code), file_name)
    if os.path.exists(filename):
      df_old = pd.read_csv(filename, encoding='gbk')
      df = pd.concat([df, df_old], axis = 0)
    df = df.drop_duplicates()

    df.to_csv(filename, encoding = 'gbk', index = False)
    print('stored north', filename)

  def get_stock_north(self):

    north_stock_status = self.datacenter.get_north_stock_status()
    stock_codes = north_stock_status['stock_code'].apply(lambda x: x[:-3]).values

    for stock_code in stock_codes:
      df = self.datacenter.get_north_stock_daily_trade(stock_code)
      self.combine_two_data(stock_code, FILE_TRADE_NORTH, df)

  def update_north_data(self, df, file_name):

    stock_codes = df['stock_code']
    for stock_code in stock_codes:
      # print("process: ", stock_code)
      data_one = df[df['stock_code'].isin([stock_code])]
      file_out = os.path.join(stock_path(self.path, stock_code.split('.')[0]), file_name)
      if os.path.exists(file_out):
        print('update_north_data: ', stock_code)
        data_file = pd.read_csv(file_out, encoding='gbk')
        data_update = pd.concat([data_one, data_file])
        data_update = data_update.sort_values(by = ['date'], ascending=False)
        data_update = data_update.drop_duplicates()
        data_update.to_csv(file_out, encoding = 'gbk', index = False)
      else:
        print('write update_north_data: ', stock_code)
        data_one.to_csv(file_out, encoding = 'gbk', index = False)

  def update_north_file(self, datacenter_func, folder, file_name, start_date = '2020-01-01', end_date = str(datetime.date.today())[0:10], board_type = 5):
    temp_path = os.path.join(self.path, folder)
    if not os.path.exists(temp_path):
      os.makedirs(temp_path)
      date_series = pd.date_range(start = start_date, end = end_date)
      for date in date_series:
        date_str = str(date)[0:10]
        df = datacenter_func(date = date_str, board_type = board_type)
        print('download north index successfully: ', date_str)
        if len(df) > 0:
          df.to_csv(os.path.join(temp_path, date_str + '.csv'), encoding = 'gbk', index = False)

      files = os.listdir(temp_path)
      for file in files:
        print('process file: ', file)
        df = pd.read_csv(os.path.join(temp_path, file), encoding = 'gbk')
        self.update_north_data(df, file_name)
    else:
      date_strs = pd.date_range(end=end_date, periods=4)
      for date_str in date_strs:
        df = datacenter_func(date = date_str, board_type = board_type)
        if (len(df) > 0):
          print('download north index successfully: ', date_str)
          self.update_north_data(df, file_name)
      
      # files = os.listdir(temp_path)
      # for file in files:
      #   print('process file: ', file)
      #   df = pd.read_csv(os.path.join(temp_path, file), encoding = 'gbk')
      #   self.update_north_data(df, file_name)

  def get_stock_north_index(self):
    # indurstry
    self.update_north_file(self.datacenter.get_north_stock_index, FOLDER_NORTH_INDEX_TEMP, FILE_INDEX_NORTH_DAILY_TRADE, 5)
    # concept
    self.update_north_file(self.datacenter.get_north_stock_index, FOLDER_NORTH_INDEX_CONCEPT_TEMP, FILE_INDEX_NORTH_DAILY_TRADE, 4)

  def get_stock_north_new(self):
    self.update_north_file(self.datacenter.get_north_stock_status, FOLDER_NORTH_STOCK_TEMP, FILE_TRADE_NORTH_NEW, start_date = '2022-07-01')



  def get_stock_margin_short(self):

    margin_short_stock_status = self.datacenter.get_margin_short_stock_status()
    stock_codes = margin_short_stock_status['stock_code'].apply(lambda x: x[:-3]).values
    for stock_code in stock_codes:
      df = self.datacenter.get_margin_short_stock(stock_code)
      filename = os.path.join(stock_path(self.path, stock_code), FILE_TRADE_MAEGIN_SHORT)
      df.to_csv(filename, encoding = 'gbk', index = False)
      print('stored north', filename)
  
  def get_stock_bill(self):

    push2_98 = ef.stock.push2_98_getter.push2_98()
    all_stock_status = push2_98.get_all_stock_status()
    stock_codes = sorted(all_stock_status['stock_code'], reverse=True)

    for stock_code in stock_codes:
      change_stock_code = stock_code[2:]
      print('download bill stock_code', change_stock_code)
      df = ef.stock.get_history_bill(change_stock_code)
      df["股票代码"] = df["股票代码"].apply(lambda x: add_stock_sh_sz_bj(x))
      df = df.sort_values(by = ['日期'], ascending=False)
      self.combine_two_data(change_stock_code, FILE_STOCK_BILL, df)

  
  def get_stock_big_deal(self):

    push2_98 = ef.stock.push2_98_getter.push2_98()
    all_stock_status = push2_98.get_all_stock_status()
    stock_codes = sorted(all_stock_status['stock_code'], reverse=True)

    for stock_code in stock_codes:
      change_stock_code = stock_code[2:]
      print('download bigdeal stock_code', change_stock_code)
      df = self.datacenter.get_stock_big_deal(change_stock_code)
      if len(df) > 0:
        path = os.path.join(stock_path(self.path, change_stock_code), FILE_STOCK_BIG_DEAL)
        df.to_csv(path, encoding = 'gbk', index = False)
        print('store ', path)


