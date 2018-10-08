# coding: utf8
'''
Created on 2018年9月23日

@author: intel
'''
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
from sklearn.cluster import spectral_clustering
from sklearn.cluster import AgglomerativeClustering
from financial_factor_calc import finance_index_dic as FID
from financial_factor_io import financial_factor_io as FIO
from stock_codes_utility import stock_codes_utility as SCU
import financial_download
import os
import sys, getopt

class financial_factor_cluster:
  def __init__(self, path = '../../../data/', path_factor = '../../../data/factor_io',
               path_cluster='../../../data/factor_cluster',
               stocks = ['000001'], dates=['2018-06-30'], indexs=['roe'],alg = 'kmean',file_name = '1806_1712_1'):
    self.stocks = stocks
    self.dates = dates
    self.indexs = indexs
    fio = FIO(path=path, path_factor=path_factor, stocks = stocks, dates = dates, file_name = file_name)
    
    if not os.path.exists(path_cluster):
      os.makedirs(path_cluster)
    self.fetch_factors = fio.fetch_selected_factors(indexs, dates)
    self.path_cluster = os.path.join(path_cluster,'{}'.format(alg)+'_cluster_{}.csv')
    self.alg = alg
    
  def cluster_financial_indexs(self, k):
    #fecth_indexs = FIR.fetch_selected_financial_indexs(indexs, self.dates)
    #date = '2017-12-31'
    date = dates[0]
    print('cluster is', date)
   # k = 10
    if self.alg=='kmean':
      km = KMeans(n_clusters=k, random_state=42)
      km.fit(self.fetch_factors.values)
      labels = km.labels_
    else:
      ward = AgglomerativeClustering(n_clusters=k, linkage='ward')
      ward.fit(self.fetch_factors.values)
      labels = ward.labels_
      
    #labels = spectral_clustering(self.fetch_factors[date].values, n_clusters=k,
    # assign_labels='discretize', random_state=1)

    self.fetch_factors["Cluster"] = labels
    #self.fetch_factors[date]["Cluster"].sort(key='Cluster', reverse=False)
    self.fetch_factors = self.fetch_factors.sort_values("Cluster",axis=0,ascending=True)
    self.fetch_factors.to_csv(self.path_cluster.format(date))
    print('save folder is', self.path_cluster.format(date))

#python financial_factor_cluster.py -o ../../../data/score/k100 -k 100 -d 2017-12-31 -a Agglomerative
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
  path = '../../../data/'
  path_factor = '../../../data/factor_io'
  path_cluster = outputfile
  scu = SCU(path=path)
  stocks = scu.stock_codes_remove_no_stock_basic()
  #stocks = ['000001','000002','000004','000005','000006']
  dates = ['2018-06-30','2017-12-31']
  #k = 300
  #FIR = financial_index_rank(path=path, path_score=path_score, stocks = stocks, dates = dates)
  indexs = [
    #earning capacity
    FID['roe'],\
    FID['roa'],\
    FID['profit_revenue'],\
    #FID['profit_cost'],\
    #FID['equlity_incr_rate'],\
    ###grow capacity
    #FID['revenue_incr_rate'],\
    #FID['profit_incr_rate'],\
    #FID['cash_incr_rate'],\
    #FID['asset_incr_rate'],
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
  path_cluster = os.path.join(path_cluster)
  FFC = financial_factor_cluster(path=path, path_factor=path_factor, path_cluster=path_cluster,\
                                  stocks=stocks,dates=dates,indexs=indexs,alg=alg,file_name = alg)
  FFC.cluster_financial_indexs(k)
  #fecth_indexs = FIR.fetch_selected_financial_indexs(indexs, dates)
  pass