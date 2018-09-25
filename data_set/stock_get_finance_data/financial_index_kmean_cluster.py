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
import sys, getopt

class financial_index_kmean_cluster:
  def __init__(self, path = '../../../data/finance_processed', path_score='../../../data/score', path_score_kmean='../../../data/score', 
               stocks = ['000001'], dates=['2018-06-30'], indexs=['roe']):
    self.path_score = path_score
    self.stocks = stocks
    self.dates = dates
    self.indexs = indexs
    FIR = financial_index_rank(path=path, path_score=path_score, stocks = stocks, dates = dates)
    
    if not os.path.exists(path_score_kmean):
      os.makedirs(path_score_kmean)
    self.feth_indexs = FIR.fetch_selected_financial_indexs(indexs, dates,path_score_kmean)
    self.path_index_score = os.path.join(path_score_kmean,'index_score_kmean_cluster_{}.csv')
    
  def kmean_financial_indexs(self, k):
    #fecth_indexs = FIR.fetch_selected_financial_indexs(indexs, self.dates)
    #date = '2017-12-31'
    for date in dates:
      print('kmean date is', date)
     # k = 10
      km = KMeans(n_clusters=k, random_state=42)
      km.fit(self.feth_indexs[date].values)
      labels = km.labels_
      self.feth_indexs[date]["Cluster"] = labels
      #self.feth_indexs[date]["Cluster"].sort(key='Cluster', reverse=False)
      self.feth_indexs[date] = self.feth_indexs[date].sort_values("Cluster",axis=0,ascending=True)
      self.feth_indexs[date].to_csv(self.path_index_score.format(date))

#python financial_index_kmean_cluster.py -o ../../../data/score/k100 -k 100
if __name__ == '__main__':
  outputfile = ''
  try:
    opts, args = getopt.getopt(sys.argv[1:],"ho:k:",["ofile=","kmean="])
  except getopt.GetoptError:
    print('test.py -o <outputfile>')
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      print('test.py -o <outputfile>')
      sys.exit()
    elif opt in ("-o", "--ofile"):
        outputfile = arg
    elif opt in ("-k", "--kmean"):
        k = int(arg)
  path = '../../../data/finance_processed'
  path_score = '../../../data/score'
  path_score_kmean = outputfile
  stocks = financial_download.ts_stock_codes()
  #stocks = ['000001','000002','000004','000005','000006']
  dates = ['2018-06-30']
  #k = 300
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
  FIKC = financial_index_kmean_cluster(path=path, path_score=path_score, path_score_kmean=path_score_kmean, stocks=stocks,dates=dates,indexs=indexs)
  FIKC.kmean_financial_indexs(k)
  #fecth_indexs = FIR.fetch_selected_financial_indexs(indexs, dates)
  pass