import os
import sys
import datetime

from ultility.common_func import *
from ultility.common_def import *
import efinance as ef
from .utils import *

class money_flow:
  def __init__(self, path):
    
    self.path = path
    if not os.path.exists(path):
      os.makedirs(path)

    self.push2_98_getter = ef.stock.push2_98_getter.push2_98()
    self.datacenter = ef.stock.datacenter()
    self.push2his = ef.stock.push2his_getter.push2his()

  def get_data_common_index_block(self, codes):

    for code in codes:
      print("download code", code)
      data = ef.stock.get_quote_history(code)
      data = data.sort_values(by = ['日期'], ascending=False)
      file = os.path.join(common_func.stock_path(self.path, code), CONST_DEF.FILE_DAILY_TRADE)
      data.to_csv(file, encoding='gbk', index = False)

  def get_index_block_data(self, indexs = ['sh', 'sz', 'sh_sz', 'cn'], blocks = ['indurstry', 'concept', 'province']):
      
    for block in blocks:
      self.get_data_common_index_block(ef_utils.get_block_codes(block))

    for index in indexs:
      self.get_data_common_index_block(ef_utils.get_block_codes(index))

  def get_north_south_history_common(self, filter, file_name):
    north_south = ef.stock.north_south_getter.north_south()
    data = north_south.north_south_history(filter)
    file = os.path.join(self.path, file_name)
    data.to_csv(file, encoding='gbk', index = False)
    print('stored ', file)

  def get_north_south_history(self):
    self.get_north_south_history_common('001', CONST_DEF.FILE_NORTH_SH)
    self.get_north_south_history_common('002', CONST_DEF.FILE_SOUTH_SH)
    self.get_north_south_history_common('003', CONST_DEF.FILE_NORTH_SZ)
    self.get_north_south_history_common('004', CONST_DEF.FILE_SOUTH_SZ)

  def combine_two_data(self, stock_code, file_name, df):

    filename = os.path.join(common_func.stock_path(self.path, stock_code), file_name)
    if os.path.exists(filename):
      df_old = pd.read_csv(filename, encoding='gbk')
      df = pd.concat([df, df_old], axis = 0)
    df = df.drop_duplicates()

    if len(df) > 0:
      df.to_csv(filename, encoding = 'gbk', index = False)
      print('stored file: ', filename)

  def get_stock_north(self):

    stock_codes = ef_utils.get_north_stock_codes()

    for stock_code in stock_codes:
      df = self.datacenter.get_north_stock_daily_trade(stock_code)
      self.combine_two_data(stock_code, CONST_DEF.FILE_TRADE_NORTH, df)

  def get_stock_north_new(self, download_days = 2):
    trade_dates = ef_utils.get_trading_date()[:100]
    self.update_north_file(self.datacenter.get_north_stock_status, CONST_DEF.FOLDER_NORTH_STOCK_TEMP, CONST_DEF.FILE_TRADE_NORTH_NEW, trade_dates, download_days = download_days)

  def update_north_data(self, df, file_name):

    stock_codes = df['stock_code']
    for stock_code in stock_codes:
      # print("process: ", stock_code)
      data_one = df[df['stock_code'].isin([stock_code])]
      file_out = os.path.join(common_func.stock_path(self.path, stock_code.split('.')[0]), file_name)
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

  def update_north_file(self, datacenter_func, folder, file_name, trade_dates = ['2022-11-08'], board_type = 5, download_days = 2):
    temp_path = os.path.join(self.path, folder)
    if not os.path.exists(temp_path):
      os.makedirs(temp_path)
      for date in trade_dates:
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
      for date in trade_dates[:download_days]:
        df = datacenter_func(date = date, board_type = board_type)
        if (len(df) > 0):
          print('download north index successfully: ', date)
          self.update_north_data(df, file_name)
      
      # files = os.listdir(temp_path)
      # for file in files:
      #   print('process file: ', file)
      #   df = pd.read_csv(os.path.join(temp_path, file), encoding = 'gbk')
      #   self.update_north_data(df, file_name)

  def get_stock_north_index(self):
    trade_dates = ef_utils.get_trading_date()[:400]
    # indurstry
    self.update_north_file(self.datacenter.get_north_stock_index, CONST_DEF.FOLDER_NORTH_INDEX_TEMP, CONST_DEF.FILE_INDEX_NORTH_DAILY_TRADE, trade_dates, board_type = 5)
    # concept
    self.update_north_file(self.datacenter.get_north_stock_index, CONST_DEF.FOLDER_NORTH_INDEX_CONCEPT_TEMP, CONST_DEF.FILE_INDEX_NORTH_DAILY_TRADE, trade_dates, board_type = 4)


  def get_stock_margin_short(self):

    dates = ef_utils.get_trading_date()[:2]
    for date in dates:
      margin_short_stock_status = self.datacenter.get_margin_short_stock_status(date)
      if len(margin_short_stock_status):
        stock_codes = margin_short_stock_status['stock_code'].apply(lambda x: x[:-3]).values
        for stock_code in stock_codes:
          df = self.datacenter.get_margin_short_stock(stock_code)
          filename = os.path.join(common_func.stock_path(self.path, stock_code), CONST_DEF.FILE_TRADE_MAEGIN_SHORT)
          df.to_csv(filename, encoding = 'gbk', index = False)
          print('stored north', filename)


  def get_stock_margin_short_total(self):

    df = self.datacenter.get_margin_short_total()
    filename = os.path.join(self.path, CONST_DEF.FILE_TRADE_MAEGIN_SHORT_TOTAL)
    df.to_csv(filename, encoding = 'gbk', index = False)
    print('stored margin_short total', filename)

  def get_stock_bill(self):

    stock_codes = ef_utils.get_stock_codes()

    for stock_code in stock_codes:
      if stock_code[0] == '4':
        continue
      print('download bill stock_code', stock_code)
      df = ef.stock.get_history_bill(stock_code)
      # print(df)
      df["股票代码"] = df["股票代码"].apply(lambda x: "'" + x)
      df = df.sort_values(by = ['日期'], ascending=False)
      self.combine_two_data(stock_code, CONST_DEF.FILE_STOCK_BILL, df)

  def get_shsz_big_bill(self):

    data_download = ef.stock.money_flow_getter.money_flow()
    data = data_download.get_shsz_big_bill()
    self.combine_two_data('', CONST_DEF.FILE_SHSZ_BIG_BILL, data)

  def get_stock_big_deal(self):

    stock_codes = ef_utils.get_stock_codes()

    for stock_code in stock_codes:
      df = self.datacenter.get_stock_big_deal(stock_code)
      if len(df) > 0:
        path = os.path.join(common_func.stock_path(self.path, stock_code), CONST_DEF.FILE_STOCK_BIG_DEAL)
        df.to_csv(path, encoding = 'gbk', index = False)
        print('store ', path)


