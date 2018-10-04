# coding: utf8
import pandas as pd
import numpy as np
import os
import tushare as ts
FILE_LIST = {'main':'{}_main.csv','abstract':'{}_abstract.csv','profit':'{}_profit.csv','cash':'{}_cash.csv','loans':'{}_loans.csv'}
TAIL_MARGIN = 1
class financial_load_store:
  def __init__(self, path='../../../data/', stock_codes=['000001']):
    self.path = path
    self.path_finance = os.path.join(path,'finance')
    self.path_finance_processed = os.path.join(path,'finance_processed')
    if not os.path.exists(self.path_finance_processed):
      os.makedirs(self.path_finance_processed)
    self.path_finance_processed = os.path.join(self.path_finance_processed,'{}_processed_finance.csv')
    self.path_stock_basic = os.path.join(path,'stock_basic')
    self.path_processed_stock_basic = os.path.join(path,'processed_stock_basic','{}_basic.csv')
    
    self.stock_codes = stock_codes
    #self.load_stock_basic()
  '''financial data'''
  def load_financical_data(self, stock_code,file_list):
    if not os.path.exists(self.path_finance):
      print('this folder not exist!!!')
      exec(-1)
    #file_list = ['{}_main.csv','{}_abstract.csv','{}_profit.csv','{}_cash.csv','{}_loans.csv']
    data_file = {}
    min_column = 3000
    for ite in file_list:
      ite = ite.format(stock_code)
      csv_file_path = os.path.join(self.path_finance, FILE_LIST[ite].format(stock_code))
      if os.path.exists(csv_file_path):
        data = pd.read_csv(csv_file_path, encoding='ANSI',error_bad_lines=False)
        if(data.shape[1]<min_column):
            min_column = data.shape[1]
        data = data.replace('--', 0)
        data = data.replace('_', 0)
        data = data.fillna(0)
      else:
        print('this file is not exist',FILE_LIST[ite])
        exit(-1)
      data_file[ite]=(data)
    self.min_column = min_column
    for ite in file_list:
      data_file[ite] = data_file[ite].iloc[:, : self.min_column-TAIL_MARGIN]
    return data_file
  def load_all_financial_one_stock(self, stock_code):
    file_list = ['main','abstract','profit','cash','loans']
    data = self.load_financical_data(stock_code, file_list)
    self.all_financial_one_stock = data
    return data
  def load_one_financial_one_stock(self,stock_code, file_list):
    data = self.load_financical_data(stock_code, file_list)
    return data
  def fetch_one_financial_factor_in_stock(self,table,factor):
    data = self.all_financial_one_stock[table]
    try:
      data1 = data[data['报告日期'].isin([factor])]
    except:
      data1 = data[data[' 报告日期'].isin([factor])]
    data1 = data1.values.squeeze()
    data1 = np.float32(data1[1:])
    return data1
  
  '''processed financial data'''
  def store_process_financical_data(self, data, stock_code):
    csv_file_path = self.path_finance_processed.format(stock_code)
    data.to_csv(csv_file_path, encoding='ANSI')
  def load_process_financical_data(self, stock_code):
    csv_file_path = self.path_finance_processed.format(stock_code)
    if not os.path.exists(csv_file_path):
      print('load_process_financical_data not exsit this file', stock_code)
      exit(-1)
    if os.path.exists(csv_file_path):
      data_pd = pd.read_csv(csv_file_path, encoding='ANSI')
      data_pd.index = data_pd.iloc[:,0]
    else:
      return pd.DataFrame()
    return data_pd
  
  '''basic stock data'''
  def load_all_stock_basic_one_stock(self,stock_codes):
    data_basic = {}
    for stock in stock_codes:
      path_csv = os.path.join(self.path_processed_stock_basic.format(stock))
      pd_basic = pd.read_csv(path_csv,index_col=0)
      data_basic[stock] = pd_basic
    self.stock_basic = data_basic
    return data_basic
  def fecth_one_stock_basic_in_stock(self,stock,factor):
    data = self.stock_basic[stock]
    data = data.T
    data1 = data.loc[factor].values.squeeze()
    data1 = np.float32(data1[:-TAIL_MARGIN])
    return data1
  
if __name__ == '__main__':
  path_root = '../../../data/'
  stock_codes = '000001'
  FLS = financial_load_store(path_root)

  data = FLS.load_one_financial_one_stock('000001', ['main'])
  
  #data = FLS.load_all_financial_one_stock('000001')
  
  #FLS.load_stock_basic(stock_codes)
  #data = FLS.get_data_stock_basic(stock_codes,'total_mv')
  pass