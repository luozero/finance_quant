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
      data = data.replace('--', 0)
      data = data.fillna(0)
    data_file.append(data)
  return data_file

def div_calc(a,b):
  data1 = a.values.squeeze()
  data1 = np.float32(data1[1:])
  data2 = b.values.squeeze()
  data2 = np.float32(data2[1:])
  data = data1/data2
  data = data.dot(100)
  return data

def earning_quality_calc(data_main, data_profit):
  equlity = data_main[data_main['报告日期'].isin(['股东权益不含少数股东权益(万元)'])]
  earning = data_profit[data_profit['报告日期'].isin(['净利润(万元)'])]
  cost = data_main[data_main['报告日期'].isin(['营业总成本(万元)'])]
  roe = div_calc(earning,equlity)
  asset = data_main[data_main['报告日期'].isin(['总资产(万元)'])]
  roa = div_calc(earning,asset)
  revenue = data_main[data_main['报告日期'].isin(['主营业务收入(万元)'])]
  profit_revenue = div_calc(earning,revenue)
  profit_cost = div_calc(earning,cost)
  
  return roe


if __name__ == '__main__':
  stock_code = '000001'
  data = load_financical_data('../../../data/finance', stock_code)
  data_main = data[0]

