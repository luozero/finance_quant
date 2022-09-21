# coding: utf8
import pandas as pd
import numpy as np
import os
from stock_deeplearning.ultility.download_record import download_record as DR
from stock_deeplearning.ultility.stock_codes_utility import stock_codes_utility as SCU
from stock_deeplearning.ultility.common_def import FILE_MAIN, FILE_ABSTRACT, FILE_PROFIT, FILE_CASH, FILE_LOANS, FILE_DAILY_TRADE, FILE_DAILY_TRADE_QUARTER,\
                FOLDER_DATA_DOWNLOAD, FOLDER_FACTOR

FILE_LIST = {'main': FILE_MAIN, 'abstract': FILE_ABSTRACT,'profit': FILE_PROFIT, 'cash': FILE_CASH, 'loans': FILE_LOANS, 'daily_trade_quarter': FILE_DAILY_TRADE_QUARTER}
TAIL_MARGIN = 1
class financial_load_store:
  def __init__(self, path='../../../data/', stock_codes=['000001']):
    self.path = path
    self.data_download_folder = os.path.join(path, FOLDER_DATA_DOWNLOAD)
    self.factor_folder = os.path.join(path, FOLDER_FACTOR)
    if not os.path.exists(self.factor_folder):
      os.makedirs(self.factor_folder)
    self.factor_folder = os.path.join(self.factor_folder,'{}_processed_finance.csv')

    self.path_stock_basic = os.path.join(path,'stock_basic','{}_basic.csv')
    self.path_processed_stock_basic = os.path.join(path,'processed_stock_basic','{}_basic.csv')
    
    self.stock_codes = stock_codes

    self.dr = DR(path)
    self.scu = SCU(path)
    #self.load_stock_basic()
  '''financial data'''
  def load_financical_data(self, file_list):
    if not os.path.exists(self.data_download_folder):
      print('this folder not exist!!!')
      exec(-1)
    #file_list = ['{}_main.csv','{}_abstract.csv','{}_profit.csv','{}_cash.csv','{}_loans.csv']
    data_file = {}
    min_column = 3000
    for ite in file_list:
      csv_file_path = os.path.join(self.data_download_folder, ite)
      if os.path.exists(csv_file_path):
        print("load file ", csv_file_path)

        data = pd.read_csv(csv_file_path, encoding='gbk')
        # data = pd.read_csv(csv_file_path, encoding='gbk',error_bad_lines=False)
        # find min_column for non trade data
        if (ite.find(FILE_DAILY_TRADE[2:]) == -1):
          if(data.shape[1]<min_column):
              min_column = data.shape[1]
        data = data.replace('--', 0)
        data = data.replace('_', 0)
        data = data.fillna(0)
      else:
        print('stock this file is not exist', ite)
        # self.dr.write_skip_stock(self.scu.add_stock_sh_sz(stock_code))
        data = pd.DataFrame()
        #exit(-1)
      data_file[ite]=(data)
    self.min_column = min_column
    for ite in file_list:
      if data_file[ite].empty == False:
        # loc data for non trade data
        if (ite.find(FILE_DAILY_TRADE[2:]) == -1):
          data_file[ite] = data_file[ite].iloc[:, : self.min_column-TAIL_MARGIN]
      else:
        data_file[ite] = pd.DataFrame()
    return data_file

  def load_all_financial_one_stock(self, stock_code):
    file_list = [FILE_MAIN.format(stock_code), FILE_ABSTRACT.format(stock_code), FILE_PROFIT.format(stock_code), \
      FILE_CASH.format(stock_code), FILE_LOANS.format(stock_code), FILE_DAILY_TRADE_QUARTER.format(stock_code)]
    data = self.load_financical_data(file_list)
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

  def fetch_one_trade_data_quarter_in_stock(self,table,factor):
    data = self.all_financial_one_stock[table]
    try:
      data1 = data['总市值']
    except:
      print(table, 'there is no this data')
    data1 = data1.values.squeeze()
    # data1 = np.float32(data1[1:])
    return data1
  
  '''processed financial data'''
  def store_process_financical_data(self, data, stock_code):
    csv_file_path = self.factor_folder.format(stock_code)
    data.to_csv(csv_file_path, encoding='gbk')
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
  
  '''basic stock data'''
  def load_all_stock_basic_one_stock(self,stock_codes):
    data_basic = {}
    for stock in stock_codes:
      path_csv = os.path.join(self.path_stock_basic.format(stock))
      pd_basic = pd.read_csv(path_csv,index_col=0)
      data_basic[stock] = pd_basic
    self.stock_basic = data_basic
    return data_basic
  def load_all_processed_stock_basic_one_stock(self,stock_codes):
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
    data1 = np.float32(data1)
    return data1
  
if __name__ == '__main__':
  path_root = '../../../data/'
  stock_codes = '000001'
  FLS = financial_load_store(path_root)

  data = FLS.load_one_financial_one_stock('300789', ['main'])
  
  #data = FLS.load_all_financial_one_stock('000001')
  
  #FLS.load_stock_basic(stock_codes)
  #data = FLS.get_data_stock_basic(stock_codes,'total_mv')
  pass