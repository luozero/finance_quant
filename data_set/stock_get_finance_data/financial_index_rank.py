# coding: utf8
'''
Created on 2018��9��17��

@author: ll
'''
import financial_index_calc as fic
from financial_index_calc import finance_index_dic as FID
import financial_download
import pandas as pd
import os

class financial_index_rank:
  def __init__(self,path = '../../../data/finance_processed',path_score = '../../../data/score', stocks = '000001', dates=['2018-06-30']):
    self.stock_codes = []
    self.path = path
    self.path_score = path_score
    if not os.path.exists(path_score):
            os.makedirs(path_score)
    self.path_overview_scores = os.path.join(path_score,'overview_scores_{}.csv'.format(dates[-1]))
    self.path_index = os.path.join(path_score,'index_{}.csv'.format(dates[-1]))
    self.path_index_score = os.path.join(path_score,'index_score_{}.csv'.format(dates[-1]))
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
  
  def fetch_selected_financial_indexs(self, indexs, dates):
    fecth_indexs = pd.Series(dtype=float)
    for date in dates:
      pd_indexs_path = os.path.join(self.path_score,'fecthing_finance_index_{}.csv'.format(date))
      if not os.path.exists(pd_indexs_path):
        pd_indexs = pd.DataFrame(dtype=float)
        print('fecthing date', date)
        for index in indexs:
          print('processing index is', index)
          [pd_index, pd_score] = self.assess_one_financial_index(index, [date])
          pd_indexs = pd.concat([pd_indexs, pd_index], axis=1)
        pd_indexs.to_csv(pd_indexs_path, encoding='ANSI')
      else:
        pd_indexs = pd.read_csv(pd_indexs_path)
      fecth_indexs[date] = pd_indexs
    return fecth_indexs
  
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
  path_score = '../../../data/score'
  print(fic.finance_index_dic['roe'])
  stocks = financial_download.ts_stock_codes()
  #stocks = ['000001','000002','000004','000005','000006']
  dates = ['2018-06-30']#,'2017-12-31'
  fir = financial_index_rank(path=path, path_score=path_score, stocks = stocks, dates = dates)
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
 
  
  
  fir.assess_selected_financial_index(indexs, dates)
  print('rank all the stock successfully');
  #data_dict = load_all_financial_processed_data(path)

  pass