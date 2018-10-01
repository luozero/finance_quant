#-*- coding:UTF-8 -*-
import pandas as pd
import numpy as np
import os
import tushare as ts
import financial_download

class factor_calc:
  def __init__(self, stock_code=['000001'], path='../../../data/finance'):
    if not os.path.exists(path):
      print('this folder not exist!!!')
    exec(-1)
    file_list = ['{}_main.csv','{}_abstract.csv','{}_profit.csv','{}_cash.csv','{}_loans.csv']
    data_file = []
    min_column = 3000;
    for ite in file_list:
      ite = ite.format(stock_code)
      csv_file_path = os.path.join(path, ite)
      if os.path.exists(csv_file_path):
        data = pd.read_csv(csv_file_path, encoding='ANSI',error_bad_lines=False)
        if(data.shape[1]<min_column):
            min_column = data.shape[1]
        data = data.replace('--', 0)
        data = data.fillna(0)
      else:
        print('this file is not exist',ite)
        exit(-1)
      data_file.append(data)
    for ite in range(0,5):
      data_file[ite] = data_file[ite].iloc[:, : min_column]
    return data_file