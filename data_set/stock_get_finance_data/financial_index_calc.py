# coding: utf8
import pandas as pd
import numpy as np
import os

'{}_main.csv','{}_abstract.csv','{}_profit.csv','{}_cash.csv','{}_loans.csv'

def load_financical_data(path, stock_code):
  if not os.path.exists(path):
    print('this folder not exist!!!')
    exec(-1)
  file_list = ['{}_main.csv','{}_abstract.csv','{}_profit.csv','{}_cash.csv','{}_loans.csv']
  data_file = []
  for ite in file_list:
    ite = ite.format(stock_code)
    csv_file_path = os.path.join(path, ite)
    if os.path.exists(csv_file_path):
      data = pd.read_csv(csv_file_path, encoding='ANSI')
    data_file.append(data)
  return data_file

if __name__ == '__main__':
  stock_code = '000001'
  data = load_financical_data('../../../data/finance', stock_code)
  data_main = data[0]
  equlity = data_main[data_main['报告日期'].isin(['股东权益不含少数股东权益(万元)'])]
  equlity = equlity.fillna(0)
  earning = data_main[data_main['报告日期'].isin(['净利润(万元)'])]
  earning = earning.fillna(0)
  data1 = earning.values.squeeze()
  data1 = np.float32(data1[1:])
  data2 = equlity.values.squeeze()
  data2 = np.float32(data2[1:])
  roe = data1/data2*100