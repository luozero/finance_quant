# coding: utf8
'''
Created on 2018年9月23日

@author: intel
'''
from sklearn.cluster import KMeans
from financial_index_calc import finance_index_dic as FID
from financial_index_rank import financial_index_rank
import financial_download
import os

class financial_index_kmean_cluster:
  def __init__(self, path = '../../../data/finance_processed', path_score='../../../data/score', stocks = ['000001'], dates=['2018-06-30'], indexs=['roe']):
    self.path_score = path_score
    self.stocks = stocks
    self.dates = dates
    self.indexs = indexs
    FIR = financial_index_rank(path=path, path_score=path_score, stocks = stocks, dates = dates)
    self.feth_indexs = FIR.fetch_selected_financial_indexs(indexs, dates)
    self.path_index_score = os.path.join(path_score,'index_score_kmean_cluster_{}.csv')
    
  def kmean_financial_indexs(self):
    #fecth_indexs = FIR.fetch_selected_financial_indexs(indexs, self.dates)
    #date = '2017-12-31'
    for date in dates:
      print('kmean date is', date)
      k = 100
      km = KMeans(n_clusters=k, random_state=42)
      km.fit(self.feth_indexs[date].values)
      labels = km.labels_
      self.feth_indexs[date]["Cluster"] = labels
      #self.feth_indexs[date]["Cluster"].sort(key='Cluster', reverse=False)
      self.feth_indexs[date] = self.feth_indexs[date].sort_values("Cluster",axis=0,ascending=True)
      self.feth_indexs[date].to_csv(self.path_index_score.format(date))

if __name__ == '__main__':
  path = '../../../data/finance_processed'
  path_score = '../../../data/score'
  stocks = financial_download.ts_stock_codes()
  #stocks = ['000001','000002','000004','000005','000006']
  dates = ['2018-06-30']
  #FIR = financial_index_rank(path=path, path_score=path_score, stocks = stocks, dates = dates)
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
    FID['asset_incr_rate'],
  ]
  '''
  FID['profit_revenue'],\
  FID['profit_cost'],\
  FID['equlity_incr_rate'],\
  ###grow capacity
  FID['revenue_incr_rate'],\
  FID['profit_incr_rate'],\
  FID['cash_incr_rate'],\
  FID['asset_incr_rate'],
  '''
  FIKC = financial_index_kmean_cluster(path=path, path_score=path_score, stocks=stocks,dates=dates,indexs=indexs)
  FIKC.kmean_financial_indexs()
  #fecth_indexs = FIR.fetch_selected_financial_indexs(indexs, dates)
  pass