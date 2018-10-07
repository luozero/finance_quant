# coding: utf8
'''
Created on 2018年9月23日

@author: intel
'''
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
from sklearn.cluster import spectral_clustering
from sklearn.cluster import AgglomerativeClustering
from financial_index_calc import finance_index_dic as FID
from financial_index_rank import financial_index_rank
import financial_download
import os
import sys, getopt

class financial_factor_cluster:
  def __init__(self, path = '../../../data/finance_processed', path_score='../../../data/score', path_score_cluster='../../../data/score', 
               stocks = ['000001'], dates=['2018-06-30'], indexs=['roe'],alg = 'kmean'):
    self.path_score = path_score
    self.stocks = stocks
    self.dates = dates
    self.indexs = indexs
    FIR = financial_index_rank(path=path, path_score=path_score, stocks = stocks, dates = dates)
    
    if not os.path.exists(path_score_cluster):
      os.makedirs(path_score_cluster)
    self.feth_indexs = FIR.fetch_selected_financial_indexs(indexs, dates,path_score_cluster)
    self.path_index_score = os.path.join(path_score_cluster,'index_score_{}'.format(alg)+'_cluster_{}.csv')
    self.alg = alg
    
  def cluster_financial_indexs(self, k):
    #fecth_indexs = FIR.fetch_selected_financial_indexs(indexs, self.dates)
    #date = '2017-12-31'
    for date in dates:
      print('kmean date is', date)
     # k = 10
      if self.alg=='kmean':
        km = KMeans(n_clusters=k, random_state=42)
        km.fit(self.feth_indexs[date].values)
        labels = km.labels_
      else:
        ward = AgglomerativeClustering(n_clusters=k, linkage='ward')
        ward.fit(self.feth_indexs[date].values)
        labels = ward.labels_
        
      #labels = spectral_clustering(self.feth_indexs[date].values, n_clusters=k,
      # assign_labels='discretize', random_state=1)

      self.feth_indexs[date]["Cluster"] = labels
      #self.feth_indexs[date]["Cluster"].sort(key='Cluster', reverse=False)
      self.feth_indexs[date] = self.feth_indexs[date].sort_values("Cluster",axis=0,ascending=True)
      self.feth_indexs[date].to_csv(self.path_index_score.format(date))

#python financial_factor_cluster.py -o ../../../data/score/k100 -k 100 -d 2017-12-31
if __name__ == '__main__':
  outputfile = ''
  try:
    opts, args = getopt.getopt(sys.argv[1:],"ho:k:d:a:",["ofile=","kmean=","date=", "algorithm="])
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
    elif opt in ("-d", "--date"):
        date = arg
    elif opt in ("-a", "--algorithm"):
        alg = arg
  path = '../../../data/finance_processed'
  path_score = '../../../data/score'
  path_score_cluster = outputfile
  stocks = financial_download.ts_stock_codes()
  #stocks = ['000001','000002','000004','000005','000006']
  dates = [date]
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
  path_score_cluster = os.path.join(path_score_cluster)
  FIKC = financial_factor_cluster(path=path, path_score=path_score, path_score_cluster=path_score_cluster, stocks=stocks,dates=dates,indexs=indexs,alg=alg)
  FIKC.cluster_financial_indexs(k)
  #fecth_indexs = FIR.fetch_selected_financial_indexs(indexs, dates)
  pass