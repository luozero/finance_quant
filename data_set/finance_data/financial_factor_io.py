# coding: utf8
'''
Created on 2018��9��17��

@author: ll
'''
from data_set.finance_data.financial_load_store import financial_load_store as FLS
from data_set.finance_data.financial_factor_calc import finance_index_dic as FID
import pandas as pd
import os
from ultility.stock_codes_utility import stock_codes_utility as SCU

class financial_factor_io:
  def __init__(self,path = '../../../data/',path_factor = '../../../data/factor_io', \
               stocks = '000001', dates=['2018-06-30'],file_name = '1806_1712'):
    self.stock_codes = []
    self.path = path
    self.path_factor = path_factor
    if not os.path.exists(path_factor):
            os.makedirs(path_factor)
    self.path_factor_io = os.path.join(path_factor,'fetched_factors_{}.csv'.format(file_name))
    self.financial_factors = self.load_all_financial_factor(dates,stocks)
  
  def load_all_financial_factor(self,dates,stocks):
   # stock_codes = ['000719']
    fls = FLS(path = self.path)
    data_dict = {}
    for stock_code in stocks:
      print("stock:",stock_code)
      data_finance = fls.load_process_financical_data(stock_code)
      if data_finance.empty:
        print('skip this stock', stock_code)
        continue
      if sum(data_finance.index.isin(dates))!=len(dates):
        print('skip this stock', stock_code)
        continue
      self.stock_codes.append(stock_code)
      data_dict[stock_code] = data_finance
    return data_dict
  
  def fetch_one_factor(self, factor, dates):
    factor_value = pd.DataFrame(dtype = float)
    column = []
    column_flag =True
    for stock_code in self.stock_codes:
      factor_temp = []
      for date in dates:
        if column_flag==True:
          column.append(factor+date)
        print('date',date,'stock_code',stock_code)
        factor_temp.append(self.financial_factors[stock_code].loc[date,factor])
      column_flag = False
      factor_value = pd.concat([factor_value, pd.DataFrame([factor_temp])],axis=0)
      #factor_value = factor_value.append(factor_temp,index = stock_code)
    return factor_value, column
  
  def fetch_selected_factors(self, factors, dates):
    if not os.path.exists(self.path_factor_io):
      pd_factor_values = pd.DataFrame(dtype=float)
      list_columns = []
      for factor in factors:
        print('processing factor is', factor)
        factor_value, column = self.fetch_one_factor(factor, dates)
        list_columns = list_columns + column
        pd_factor_values = pd.concat([pd_factor_values, factor_value], axis=1)
      pd_factor_values.columns = list_columns
      scu = SCU(path=self.path)
      pd_factor_values.index = scu.add_allstock_sh_sz(self.stock_codes)
      pd_factor_values.to_csv(self.path_factor_io, encoding='gbk')
    else:
      pd_factor_values = pd.read_csv(self.path_factor_io,index_col=0)
    return pd_factor_values
 
    
if __name__ == '__main__':
  path = '../../../data/'
  path_factor = '../../../data/factor_io'
  print(FID['roe'])
  scu = SCU(path=path)
  stocks = scu.stock_codes_remove_no_stock_basic()
  stocks = ['000001','000002','000004','000005','000006']
  dates = ['2018-06-30','2017-12-31']#,'2017-12-31'
  ffio = financial_factor_io(path=path, path_factor=path_factor, \
                             stocks = stocks, dates = dates,file_name = '1806_1712_1')
  indexs = [
    #earning capacity
    FID['roe'],\
    FID['roa'],\
    FID['profit_revenue'],\
    FID['profit_cost'],\
    FID['equlity_incr_rate'],\
    ###grow capacity
    FID['revenue_incr_rate'],\
    FID['profit_incr_rate'],\
    FID['cash_incr_rate'],\
    FID['asset_incr_rate'],\
  ]
  """ 
  FID['debt_incr_rate'],\
  ###asset struct
  FID['debt_asset_ratio'],\
  FID['debt_equality_ratio'],\
  FID['debt_net_asset_ratio'],\
  FID['revenue_asset_ratio'],\
  FID['goodwell_equality_ratio'],\
  FID['dev_rev_ratio']\
  """
 
  
  
  ffio.fetch_selected_factors(indexs, dates)
  print('rank all the stock successfully');
  #data_dict = load_all_financial_processed_data(path)

  pass