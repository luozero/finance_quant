# coding: utf8
import pandas as pd
import numpy as np
import os
from ultility.common_def import * 
from ultility.common_func import *

FILE_LIST = {'main': FILE_MAIN, 'abstract': FILE_ABSTRACT,'profit': FILE_PROFIT, 'cash': FILE_CASH, 'loans': FILE_LOANS, 'daily_trade_quarter': FILE_DAILY_TRADE_QUARTER}
TAIL_MARGIN = 1
class finance_load_store:
  def __init__(self, path_finance = 'finance', path_factor = 'path_factor', stock_codes='000001'):

    self.path_finance = path_finance

    self.factor_folder = path_factor
    if not os.path.exists(self.factor_folder):
      os.makedirs(self.factor_folder)
    self.factor_folder = os.path.join(self.factor_folder,'{}_processed_finance.csv')

    #self.load_stock_basic()
  '''finance data'''
  def load_one_finance_data(self, file_list):
    if not os.path.exists(self.path_finance):
      print('this folder not exist!!!')
      exec(-1)
    #file_list = ['{}_main.csv','{}_abstract.csv','{}_profit.csv','{}_cash.csv','{}_loans.csv']
    data_file = {}
    min_column = 3000
    for ite in file_list:
      data = read_csv(self.path_finance, ite)
      # find min_column for non trade data
      if (ite.find('daily_trade') == -1):
        if(data.shape[1]<min_column):
            min_column = data.shape[1]

      data_file[ite]=(data)
    self.min_column = min_column
    for ite in file_list:
      if data_file[ite].empty == False:
        # loc data for non trade data
        if (ite.find('daily_trade') == -1):
          data_file[ite] = data_file[ite].iloc[:, : self.min_column-TAIL_MARGIN]
      else:
        data_file[ite] = pd.DataFrame()
    return data_file

  def load_all_finance_data(self, stock_code):
    file_list = [FILE_MAIN.format(stock_code), FILE_ABSTRACT.format(stock_code), FILE_PROFIT.format(stock_code), \
      FILE_CASH.format(stock_code), FILE_LOANS.format(stock_code), FILE_DAILY_TRADE_QUARTER.format(stock_code)]
    data = self.load_one_finance_data(file_list)
    self.all_finance_one_stock = data
    return data

  def load_one_finance_one_stock(self,stock_code, file_list):
    data = self.load_one_finance_data(stock_code, file_list)
    return data

  def fetch_one_finance_factor_in_stock(self,table,factor):
    data = self.all_finance_one_stock[table]
    try:
      data1 = data[data['报告日期'].isin([factor])]
    except:
      data1 = data[data[' 报告日期'].isin([factor])]
    data1 = data1.values.squeeze()
    data1 = np.float32(data1[1:])
    return data1

  def fetch_one_trade_data_quarter_in_stock(self,table,factor):
    data = self.all_finance_one_stock[table]
    try:
      data1 = data['总市值']
    except:
      print(table, 'there is no this data')
    data1 = data1.values.squeeze()
    # data1 = np.float32(data1[1:])
    return data1
  
  '''processed finance data'''
  def store_process_financical_data(self, data, stock_code):
    csv_file_path = self.factor_folder.format(stock_code)
    data.to_csv(csv_file_path, encoding='gbk')
    print("finance factor store to ", csv_file_path)

  def load_process_financical_data(self, stock_code):
    csv_file_path = self.factor_folder.format(stock_code)
    if not os.path.exists(csv_file_path):
      print('load_process_financical_data not exsit this file', stock_code)
      exit(-1)
    if os.path.exists(csv_file_path):
      data_pd = pd.read_csv(csv_file_path, encoding='gbk')
      data_pd.index = data_pd.iloc[:,0]
    else:
      return pd.DataFrame()
    return data_pd
  
  # def fecth_one_stock_basic_in_stock(self,stock,factor):
  #   data = self.stock_basic[stock]
  #   data = data.T
  #   data1 = data.loc[factor].values.squeeze()
  #   data1 = np.float32(data1)
  #   return data1
  
if __name__ == '__main__':
  path_root = '../../../data/'
  stock_codes = '000001'
  FLS = finance_load_store(path_root)

  data = FLS.load_one_finance_one_stock('300789', ['main'])
  
  #data = FLS.load_all_finance_data('000001')
  
  #FLS.load_stock_basic(stock_codes)
  #data = FLS.get_data_stock_basic(stock_codes,'total_mv')
  pass