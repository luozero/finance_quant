# coding: utf8
'''
Created on 2018��9��17��

@author: ll
'''
import financial_index_calc
import financial_download
import pandas as pd
import os

class financial_index_rank:
  def __init__(self,path = '../../../data/finance_processed',path_rs = '../../../data/score'):
    self.stock_codes = financial_download.ts_stock_codes()
    self.path = path
    if not os.path.exists(path_rs):
            os.makedirs(path_rs)
    self.path_overview_scores = os.path.join(path_rs,'overview_scores.csv')
    self.path_index = os.path.join(path_rs,'index.csv')
    self.path_index_score = os.path.join(path_rs,'index_score.csv')
    self.financial_index_data = self.load_all_financial_index()
  
  def load_all_financial_index(self):
   # stock_codes = ['000719']
    data_dict = {}
    for stock_code in self.stock_codes:
      print("stock:",stock_code)
      data_finance = financial_index_calc.load_process_financical_data(self.path, stock_code)
      if data_finance.empty:
        continue
      data_dict[stock_code] = data_finance
    return data_dict
  
  def assess_one_financial_index(self, index, dates, stocks):
    index_dict = {}
    score_dict = {}
    len_dates = len(dates)
    for stock_code in stocks:
      index_dict[stock_code] = 0
      for date in dates:
        index_dict[stock_code] = index_dict[stock_code] + \
        self.financial_index_data[stock_code].loc[date,index]
      index_dict[stock_code]  = index_dict[stock_code] / len_dates;
    index_dict_sorted = sorted(index_dict.items(), key = lambda d:d[1],reverse = True)
    stock_len = len(index_dict_sorted)
    rank_index=0
    for key, val in index_dict_sorted:
      score_dict[key] = (stock_len-rank_index)/stock_len * 100
      rank_index = rank_index + 1
    score_dict = sorted(score_dict.items(), key = lambda d:d[0],reverse = True)
    return [pd.DataFrame.from_dict(index_dict), pd.DataFrame.from_dict(score_dict)]
  
  def assess_selected_financial_index(self,indexs,dates,stocks):
    pd_indexs = pd.DataFrame()
    pd_scores = pd.DataFrame()
    for index in indexs:
      [pd_index, pd_score] = self.assess_one_financial_index(index, dates, stocks)
      pd_indexs = pd.concat([pd_indexs, pd_index], axis=1)
      pd_scores = pd.concat([pd_scores, pd_score], axis=1)
    
    pd_mean_scores = pd_scores.mean(axis=1)
    pd_mean_scores.to_csv(self.path_overview_scores, encoding='ANSI')
    pd_scores.to_csv(self.path_index_score, encoding='ANSI')
    pd_indexs.to_csv(self.path_index, encoding='ANSI')
    
      
    
if __name__ == '__main__':
  path = '../../../data/finance_processed'
  path_rs = '../../../data/score'
  print(financial_index_calc.finance_index_dic['roe'])
  fir = financial_index_rank(path=path, path_rs=path_rs)
  indexs = financial_index_calc.finance_index_dic['roe']
  dates = '2018/6/30'
  stocks = ['000001','000002']
  fir.assess_selected_financial_index(indexs, dates, stocks)
  #data_dict = load_all_financial_processed_data(path)

  pass