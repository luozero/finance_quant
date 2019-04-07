# coding: utf8
import pandas as pd
import numpy as np
import os
import tushare as ts
import financial_download

finance_index_dic = {
  #####earning capacity
  'roe':'roe','roa':'roa','profit_revenue':'profit_revenue','profit_cost':'profit_cost','equlity_incr_rate':'equlity_incr_rate',
  ###grow capacity
  'revenue_incr_rate':'revenue_incr_rate','profit_incr_rate':'profit_incr_rate',
  'cash_incr_rate':'cash_incr_rate','asset_incr_rate':'asset_incr_rate','debt_incr_rate':'debt_incr_rate',
  ###asset struct
  'debt_asset_ratio':'debt_asset_ratio','debt_equality_ratio':'debt_equality_ratio','debt_net_asset_ratio':'debt_net_asset_ratio',
  'revenue_asset_ratio':'revenue_asset_ratio','goodwell_equality_ratio':'goodwell_equality_ratio','dev_rev_ratio':'dev_rev_ratio',
  ##enterprise value
  'CFO2EV':'CFO2EV','EDITDA2EV':'EDITDA2EV',
  'E2PFY0':'E2PFY0','E2PFY1':'E2PFY1',
  'BB2P':'BB2P','BB2EV':'BB2EV',
  'B2P':'B2P','S2EV':'S2EV',
  ##quality
  'RNOA':'RNOA','CFROI':'CFROI','OL':'OL','OLinc':'OLinc','WCinc':'WCinc','NCOinc':'NCOinc',
  'icapx':'icapx','capxG':'capxG','XF':'XF','shareInc':'shareInc',
  }

def load_financical_data(path, stock_code):
  if not os.path.exists(path):
    print('this folder not exist!!!')
    exec(-1)
  file_list = ['{}_main.csv','{}_abstract.csv','{}_profit.csv','{}_cash.csv','{}_loans.csv']
  data_file = []
  min_column = 3000
  for ite in file_list:
    ite = ite.format(stock_code)
    csv_file_path = os.path.join(path, ite)
    if os.path.exists(csv_file_path):
      data = pd.read_csv(csv_file_path, encoding='gbk',error_bad_lines=False)
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

def store_process_financical_data(path, data, stock_code):
  if not os.path.exists(path):
    os.makedirs(path)
  file_list = '{}_processed_finance.csv'.format(stock_code)
  csv_file_path = os.path.join(path, file_list)
  data.to_csv(csv_file_path, encoding='gbk')
def load_process_financical_data(path, stock_code):
  if not os.path.exists(path):
    os.makedirs(path)
  file_list = '{}_processed_finance.csv'.format(stock_code)
  csv_file_path = os.path.join(path, file_list)
  if os.path.exists(csv_file_path):
    data_pd = pd.read_csv(csv_file_path, encoding='gbk')
    data_pd.index = data_pd.iloc[:,0]
  else:
    return pd.DataFrame()
  return data_pd
def ab_ratio_calc(a,b,str):
  data1 = a.values.squeeze()
  data1 = np.float32(data1[1:])
  data2 = b.values.squeeze()
  data2 = np.float32(data2[1:])
  data = data1/data2
  data[np.isinf(data)]=0
  data[np.isnan(data)]=0
  data = data.dot(100)
  dict_data = {str:data}
  pd_data = pd.DataFrame(dict_data)
  return pd_data
def qoq_rate_calc(a,str):
  data1 = a.values.squeeze()
  data1 = np.float32(data1[1:])
  data = (data1[:-4]-data1[4:])/data1[4:]
  data = data.dot(100)
  data[np.isinf(data)]=0
  data = np.append(data,[0,0,0,0])
  dict_data = {str:data}
  pd_data = pd.DataFrame(dict_data)
  return pd_data
def abc_ratio_calc(a,b,c,str,op):
  data1 = a.values.squeeze()
  data1 = np.float32(data1[1:])
  data2 = b.values.squeeze()
  data2 = np.float32(data2[1:])
  data3 = c.values.squeeze()
  data3 = np.float32(data3[1:])
  if(op=='sub'):
    data = data1/(data2-data3)
  data[np.isinf(data)]=0
  dict_data = {str:data}
  pd_data = pd.DataFrame(dict_data)
  return pd_data

def financial_index_calc(data):
  data_main = data[0]
  data_abstract = data[1]
  data_profit = data[2]
  data_cash = data[3]
  data_loan = data[4]
  equlity = data_main[data_main['报告日期'].isin(['股东权益不含少数股东权益(万元)'])]
  asset = data_main[data_main['报告日期'].isin(['总资产(万元)'])]
  revenue = data_main[data_main['报告日期'].isin(['主营业务收入(万元)'])]
  cash = data_main[data_main['报告日期'].isin(['经营活动产生的现金流量净额(万元)'])]
  debt = data_main[data_main['报告日期'].isin(['总负债(万元)'])]
  
  earning = data_profit[data_profit['报告日期'].isin(['净利润(万元)'])]
  cost = data_profit[data_profit['报告日期'].isin(['营业总成本(万元)'])]
 
  equality = data_loan[data_loan['报告日期'].isin(['所有者权益(或股东权益)合计(万元)'])]
  intangible_asset = data_loan[data_loan['报告日期'].isin(['无形资产(万元)'])]
  dev_cost = data_loan[data_loan['报告日期'].isin(['开发支出(万元)'])]
  goodwell = data_loan[data_loan['报告日期'].isin(['商誉(万元)'])]
 
  #####earning capacity
  #roe
  roe = ab_ratio_calc(earning,equlity,'roe')
  pd_data = roe
  #roa
  roa = ab_ratio_calc(earning,asset,'roa')
  pd_data = pd.concat([pd_data, roa], axis=1)
  #profit_revenue
  profit_revenue = ab_ratio_calc(earning,revenue,finance_index_dic['profit_revenue'])
  pd_data = pd.concat([pd_data, profit_revenue], axis=1)
  #profit_cost
  profit_cost = ab_ratio_calc(earning,cost,finance_index_dic['profit_cost'])
  pd_data = pd.concat([pd_data, profit_cost], axis=1)
  #stackholder equality increase
  equlity_incr_rate = qoq_rate_calc(equality,finance_index_dic['equlity_incr_rate'])
  pd_data = pd.concat([pd_data, equlity_incr_rate], axis=1)

  ###grow capacity
  #revenue
  revenue_incr_rate = qoq_rate_calc(revenue,finance_index_dic['revenue_incr_rate'])
  pd_data = pd.concat([pd_data, revenue_incr_rate], axis=1)
  #profit
  profit_incr_rate = qoq_rate_calc(earning,finance_index_dic['profit_incr_rate'])
  pd_data = pd.concat([pd_data, profit_incr_rate], axis=1)
  #cash
  cash_incr_rate = qoq_rate_calc(cash,finance_index_dic['cash_incr_rate'])
  pd_data = pd.concat([pd_data, cash_incr_rate], axis=1)
  #asset
  asset_incr_rate = qoq_rate_calc(asset,finance_index_dic['asset_incr_rate'])
  pd_data = pd.concat([pd_data, asset_incr_rate], axis=1)
  #debt
  debt_incr_rate = qoq_rate_calc(debt,finance_index_dic['debt_incr_rate'])
  pd_data = pd.concat([pd_data, debt_incr_rate], axis=1)
  
  ###asset struct
  #debt_asset_ratio
  debt_asset_ratio = ab_ratio_calc(debt,asset,finance_index_dic['debt_asset_ratio'])
  debt_asset_ratio = debt_asset_ratio/100
  pd_data = pd.concat([pd_data, debt_asset_ratio], axis=1)
  #debt_equality_ratio
  debt_equality_ratio = ab_ratio_calc(debt,equality,finance_index_dic['debt_equality_ratio'])
  debt_equality_ratio = debt_equality_ratio/100
  pd_data = pd.concat([pd_data, debt_equality_ratio], axis=1)
  #debt_net_asset_ratio
  debt_net_asset_ratio = abc_ratio_calc(debt,equality,intangible_asset,finance_index_dic['debt_net_asset_ratio'],'sub')
  pd_data = pd.concat([pd_data, debt_net_asset_ratio], axis=1)
  #revenue_asset_ratio
  revenue_asset_ratio = ab_ratio_calc(revenue,asset,finance_index_dic['revenue_asset_ratio'])
  revenue_asset_ratio = revenue_asset_ratio
  pd_data = pd.concat([pd_data, revenue_asset_ratio], axis=1)
  #goodwell_equality_ratio
  goodwell_equality_ratio = ab_ratio_calc(goodwell,equality,finance_index_dic['goodwell_equality_ratio'])
  pd_data = pd.concat([pd_data, goodwell_equality_ratio], axis=1)
  
  ###CFO2EV
  dev_rev_ratio = ab_ratio_calc(cash,revenue,finance_index_dic['CFO2EV'])
  pd_data = pd.concat([pd_data, dev_rev_ratio], axis=1)
  
  pd_data.index = data_main.iloc[0,:].index[1:]
  return pd_data #pd.DataFrame([roe roa profit_revenue profit_cost])

def main_financial_data_process(path, path_res):
  stock_codes = financial_download.ts_stock_codes()
 # stock_codes = ['000719']
  for stock_code in stock_codes:
    print("stock:",stock_code)
    data_finance = load_financical_data(path, stock_code)
    data_processed = financial_index_calc(data_finance)
    store_process_financical_data(path_res, data_processed, stock_code)
  
if __name__ == '__main__':
  #stock_codes = ['000001','000002','000004']
  
  path = '../../../data/finance'
  path_res = '../../../data/finance_processed'
  main_financial_data_process(path, path_res)
  print("processed successfully!!!")
 # data_main = data[0]

