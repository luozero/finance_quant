# coding: utf8
'''
Created on 2018��9��17��

@author: ll
'''
import data_set.finance_data.finance_factor_calc as FFC
from data_set.finance_data.finance_factor_calc import finance_index_dic as FID
from data_set.finance_data.finance_factor_io import finance_factor_io as FIO
from ultility.stock_codes_utility import stock_codes_utility as SCU
from ultility.common_def import *
import pandas as pd
import os
import sys, getopt

class finance_factor_rank:
  def __init__(self, path_factor = 'path_factor', path_rank = 'path_rank',
               stocks = ['000001'], dates=['2018-06-30'], indexs=['roe'],file_name = '1806_1712_1'):

    self.stocks = stocks
    self.dates = dates
    self.indexs = indexs
    fio = FIO(path_factor=path_factor, stocks = stocks, dates = dates, file_name = file_name)
    
    if not os.path.exists(path_rank):
      os.makedirs(path_rank)
    self.fetch_factors = fio.fetch_selected_factors(indexs, dates)
    self.path_rank = os.path.join(path_rank, file_name)
  
  def load_all_finance_index(self,dates,stocks):
   # stock_codes = ['000719']
    data_dict = {}
    for stock_code in stocks:
      print("stock:",stock_code)
      data_finance = FFC.load_process_financical_data(self.path, stock_code)
      if data_finance.empty:
        print('skip this stock', stock_code)
        continue
      if sum(data_finance.index.isin(dates))!=len(dates):
        print('skip this stock', stock_code)
        continue
      self.stock_codes.append(stock_code)
      data_dict[stock_code] = data_finance
    return data_dict
  
  def assess_one_finance_factor(self, index):
    score_series = pd.Series(dtype=float)
    #len_dates = len(dates)
    factor_series = self.fetch_factors.loc[:,index]
    factor_series_sorted = factor_series.sort_values(axis=0,ascending=False) #sorted(factor_series.items(), key = lambda d:d[1],reverse = True)
    stock_len = len(factor_series_sorted)
    rank_index=0
    for stock in factor_series_sorted.index:
      score_series[stock] = float(stock_len-rank_index)/float(stock_len) * 100.0
      rank_index = rank_index + 1
    score_series = score_series.sort_index(axis=0,ascending=True)#sorted(score_series.items(), key = lambda d:d[0],reverse = True)
    return [pd.DataFrame({index:factor_series}), pd.DataFrame({index:score_series})]
    
  def assess_selected_finance_factor(self,dates):
    pd_indexs = pd.DataFrame()
    pd_scores = pd.DataFrame()
    for index in self.fetch_factors.columns:
      print('processing index is', index)
      [pd_index, pd_score] = self.assess_one_finance_factor(index)
      pd_indexs = pd.concat([pd_indexs, pd_index], axis=1)
      pd_scores = pd.concat([pd_scores, pd_score], axis=1)
    
    pd_mean_scores = pd_scores.mean(axis=1)
    #pd_mean_scores = pd_mean_scores.sort_values(axis=0,ascending=False)
    # pd_indexs['rank'] = pd_mean_scores.values
    pd_rank = pd.DataFrame(pd_mean_scores.values, columns=['rank'], index = pd_indexs.index)
    pd_indexs = pd.concat([pd_indexs, pd_rank], axis=1)

    print(pd_indexs)

    pd_indexs = pd_indexs.sort_values("rank",axis=0,ascending=False)
    pd_indexs.to_csv(self.path_rank, encoding='gbk')
    print(self.path_rank)


def finance_factors_rank(path_finance_factor, path_finance_rank, filename = 'rank_result', stock_codes = ['000001'],
                           dates = ['2018-09-30'], factors = [FID['roe'], FID['roa']]):

  ffr = finance_factor_rank(path_factor=path_finance_factor, path_rank=path_finance_rank, stocks=stock_codes, dates=dates,
                              indexs=factors, file_name=filename)
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

  ffr.assess_selected_finance_factor(dates)
  print('rank all the stock successfully');
      
#python finance_factor_rank.py -f rank_output
if __name__ == '__main__':
  path = '../../../data/finance_processed'
  path_score = '../../../data/score'
  outputfile = ''
  filename = 'test'
  try:
    opts, args = getopt.getopt(sys.argv[1:],"f:",["filename="])
  except getopt.GetoptError:
    print('test.py -o <outputfile>')
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      print('test.py -o <outputfile>')
    elif opt in ("-f", "--filename"):
      filename = arg
  path = '../../../data/'
  path_rank = '../../../data/factor_rank'
  path_factor = '../../../data/factor_io'
  path_cluster = outputfile
  
  scu = SCU(path=path)
  stocks = scu.stock_codes_remove_no_stock_basic()
  #stocks = ['000001','000002','000004','000005','000006']
  indexs = [
    #earning capacity
    FID['roe'],\
    FID['roa'],\
    FID['profit_revenue'],\
    FID['cash_incr_rate'],\
    #FID['profit_cost'],\
    #FID['equlity_incr_rate'],\
    #grow capacity
    #FID['revenue_incr_rate'],\
    #FID['profit_incr_rate'],\
    #FID['cash_incr_rate'],\
    #FID['asset_incr_rate'],\
  ]
  dates = ['2018-09-30','2018-06-30','2017-12-31','2016-12-31','2015-12-31','2014-12-31']#,'2017-12-31'
  dates = ['2018-09-30','2018-06-30','2018-03-31','2017-12-31','2017-09-30','2017-06-30','2017-03-31']#,'2017-12-31'
  ffr = finance_factor_rank(path=path, path_factor=path_factor, path_cluster = path_rank, stocks = stocks, dates = dates, indexs = indexs, file_name = filename)
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
 
  
  
  ffr.assess_selected_finance_factor(dates)
  print('rank all the stock successfully');
  #data_dict = load_all_finance_processed_data(path)

  pass