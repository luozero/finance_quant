# coding: utf8
'''
Created on 2018��9��17��

@author: ll
'''
import financial_index_calc as fic
from financial_index_calc import finance_index_dic as fid
import financial_download
import pandas as pd
import os

class financial_index_rank:
  def __init__(self,path = '../../../data/finance_processed',path_rs = '../../../data/score', stocks = '000001', dates=['2018-06-30']):
    self.stock_codes = []
    self.path = path
    if not os.path.exists(path_rs):
            os.makedirs(path_rs)
    self.path_overview_scores = os.path.join(path_rs,'overview_scores_{}.csv'.format(dates[-1]))
    self.path_index = os.path.join(path_rs,'index_{}.csv'.format(dates[-1]))
    self.path_index_score = os.path.join(path_rs,'index_score_{}.csv'.format(dates[-1]))
    self.financial_index_data = self.load_all_financial_index(dates,stocks)
  
  def load_all_financial_index(self,dates,stocks):
   # stock_codes = ['000719']
    data_dict = {}
    for stock_code in stocks:
      print("stock:",stock_code)
      data_finance = fic.load_process_financical_data(self.path, stock_code)
      if data_finance.empty:
        print('skip this stock', stock_code)
        continue
      if sum(data_finance.index.isin(dates))!=len(dates):
        print('skip this stock', stock_code)
        continue
      self.stock_codes.append(stock_code)
      data_dict[stock_code] = data_finance
    return data_dict
  
  def assess_one_financial_index(self, index, dates):
    index_series = pd.Series(dtype=float)
    score_series = pd.Series(dtype=float)
    len_dates = len(dates)
    for stock_code in self.stock_codes:
      index_series[stock_code] = 0.0
      for date in dates:
        print('date',date,'stock_code',stock_code)
        index_series[stock_code] = index_series[stock_code] + self.financial_index_data[stock_code].loc[date,index]
      index_series[stock_code]  = index_series[stock_code] / float(len_dates);
    index_series_sorted = index_series.sort_values(axis=0,ascending=False) #sorted(index_series.items(), key = lambda d:d[1],reverse = True)
    stock_len = len(index_series_sorted)
    rank_index=0
    for stock in index_series_sorted.index:
      score_series[stock] = float(stock_len-rank_index)/float(stock_len) * 100.0
      rank_index = rank_index + 1
    score_series = score_series.sort_index(axis=0,ascending=True)#sorted(score_series.items(), key = lambda d:d[0],reverse = True)
    return [pd.DataFrame({index:index_series}), pd.DataFrame({index:score_series})]
  
  def assess_selected_financial_index(self,indexs,dates):
    pd_indexs = pd.DataFrame()
    pd_scores = pd.DataFrame()
    for index in indexs:
      print('processing index is', index)
      [pd_index, pd_score] = self.assess_one_financial_index(index, dates)
      pd_indexs = pd.concat([pd_indexs, pd_index], axis=1)
      pd_scores = pd.concat([pd_scores, pd_score], axis=1)
    
    pd_mean_scores = pd_scores.mean(axis=1)
    pd_mean_scores = pd_mean_scores.sort_values(axis=0,ascending=False)
    pd_mean_scores.to_csv(self.path_overview_scores, encoding='ANSI')
    pd_scores.to_csv(self.path_index_score, encoding='ANSI')
    pd_indexs.to_csv(self.path_index, encoding='ANSI')
    
      
    
if __name__ == '__main__':
  path = '../../../data/finance_processed'
  path_rs = '../../../data/score'
  print(fic.finance_index_dic['roe'])
  stocks = financial_download.ts_stock_codes()
  #stocks = ['000001','000002','000004','000005','000006']
  dates = ['2018-06-30','2017-12-31']
  fir = financial_index_rank(path=path, path_rs=path_rs, stocks = stocks, dates = dates)
  indexs = [
    #earning capacity
    fid['roe'],\
    fid['roa'],\
    fid['profit_revenue'],\
    fid['profit_cost'],\
    fid['equlity_incr_rate'],\
    ###grow capacity
    fid['revenue_incr_rate'],\
    fid['profit_incr_rate'],\
    fid['cash_incr_rate'],\
    fid['asset_incr_rate'],\
  ]
  """ 
  fid['debt_incr_rate'],\
  ###asset struct
  fid['debt_asset_ratio'],\
  fid['debt_equality_ratio'],\
  fid['debt_net_asset_ratio'],\
  fid['revenue_asset_ratio'],\
  fid['goodwell_equality_ratio'],\
  fid['dev_rev_ratio']\
  """
 
  
  
  fir.assess_selected_financial_index(indexs, dates)
  print('rank all the stock successfully');
  #data_dict = load_all_financial_processed_data(path)

  pass