# coding: utf8
'''
Created on 2018年9月23日

@author: intel
'''
from sklearn.cluster import KMeans
from financial_index_calc import finance_index_dic as fid
from financial_index_rank import financial_index_rank
import financial_download

class financial_index_kmean_cluster:
  def __init__(self, path_score='../../../data/score', stocks = '000001', dates=['2018-06-30']):
    self.path_score = path_score
    self.stocks = stocks
    self.dates = dates
    self.feth_indexs = fir.fetch_selected_financial_indexs(self.indexs, self.dates)
  def kmean_financial_indexs(self,indexs):
    

if __name__ == '__main__':
  path = '../../../data/finance_processed'
  path_rs = '../../../data/score'
  stocks = financial_download.ts_stock_codes()
  stocks = ['000001','000002','000004','000005','000006']
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
  fecth_indexs = fir.fetch_selected_financial_indexs(indexs, dates)
  pass