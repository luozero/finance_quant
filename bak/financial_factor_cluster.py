# coding: utf8
'''
Created on 2018年9月23日

@author: intel
'''
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
from sklearn.cluster import spectral_clustering
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import AffinityPropagation
from sklearn.cluster import Birch
from finance_factor_calc import finance_index_dic as FID
from finance_factor_io import finance_factor_io as FIO
from ultility.stock_codes_utility import stock_codes_utility as SCU
import os
import sys, getopt

class finance_factor_cluster:
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
    self.path_cluster = os.path.join(path_cluster,'{}'.format(file_name)+'_cluster_{}.csv')
    self.alg = alg
    
  def cluster_finance_indexs(self, k):
    #fecth_indexs = FIR.fetch_selected_finance_indexs(indexs, self.dates)
    #date = '2017-12-31'
    date = dates[0]
    print('cluster is', date, 'alg is', self.alg)
   # k = 10
    X=self.fetch_factors.values

    
    if self.alg=='kmean':
      km = KMeans(n_clusters=k, random_state=42)
      km.fit(X)
      labels = km.labels_
    elif self.alg=='agglomerative':
      ward = AgglomerativeClustering(n_clusters=k, linkage='ward')
      ward.fit(X)
      labels = ward.labels_
    elif self.alg == 'DBSCAN':
      # Compute DBSCAN
      db = DBSCAN(eps=10, min_samples=10).fit(X)
      labels = db.labels_
    elif self.alg == 'spectral':
      # Compute DBSCAN
      labels = spectral_clustering(X, n_clusters=k, eigen_solver='arpack')
      #labels = db.labels_
    elif self.alg == 'birch':
      # Compute DBSCAN
      brc = Birch(threshold=50, branching_factor=50, n_clusters=300, compute_labels=True)
      labels = brc.fit(X)
      labels = labels.labels_
    elif self.alg == 'affinity':
      
      #af = AffinityPropagation(affinity='precomputed').fit(X)
      af = AffinityPropagation(max_iter=500,affinity='euclidean').fit(X)
      labels = af.labels_
    else:
      print('not support this cluster')
      exit(-1)
      
    #labels = spectral_clustering(self.fetch_factors[date].values, n_clusters=k,
    # assign_labels='discretize', random_state=1)

    self.fetch_factors["Cluster"] = labels
    #self.fetch_factors[date]["Cluster"].sort(key='Cluster', reverse=False)
    self.fetch_factors = self.fetch_factors.sort_values("Cluster",axis=0,ascending=True)
    self.fetch_factors.to_csv(self.path_cluster.format(date))
    print('save folder is', self.path_cluster.format(date))

#python finance_factor_cluster.py -o ../../../data/factor_cluster -k 100 -d 2017-12-31 -a affinity -f affinity_roe_rev_profit_cash11
if __name__ == '__main__':
  outputfile = ''
  try:
    opts, args = getopt.getopt(sys.argv[1:],"ho:k:d:a:f:",["ofile=","kmean=","date=", "algorithm=","filename="])
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
    elif opt in ("-f", "--filename"):
        filename = arg
  path = '../../../data/'
  path_factor = '../../../data/factor_io'
  path_cluster = outputfile
  scu = SCU(path=path)
  stocks = scu.stock_codes_remove_no_stock_basic()
  #stocks = ['000001','000002','000004','000005','000006']
  dates = ['2018-06-30','2017-12-31','2016-12-31']
  #k = 300
  #FIR = finance_index_rank(path=path, path_score=path_score, stocks = stocks, dates = dates)
  indexs = [
    #earning capacity
    FID['roe'],\
    FID['roa'],\
    FID['profit_revenue'],\
    FID['revenue_incr_rate'],\
    FID['cash_incr_rate'],\
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
    ##enterprise value
  'CFO2EV':'CFO2EV','EDITDA2EV':'EDITDA2EV',
  'E2PFY0':'E2PFY0','E2PFY1':'E2PFY1',
  'BB2P':'BB2P','BB2EV':'BB2EV',
  'B2P':'B2P','S2EV':'S2EV',
  'NCO2A':'NCO2A',
  'E2EV':'E2EV',
  ##quality
  'OL':'OL','OLinc':'OLinc','WCinc':'WCinc','NCOinc':'NCOinc',
  'icapx':'icapx','capxG':'capxG','XF':'XF','shareInc':'shareInc',
  '''
  path_cluster = os.path.join(path_cluster)
  FFC = finance_factor_cluster(path=path, path_factor=path_factor, path_cluster=path_cluster,\
                                  stocks=stocks,dates=dates,indexs=indexs,alg=alg,file_name = filename)
  FFC.cluster_finance_indexs(k)
  #fecth_indexs = FIR.fetch_selected_finance_indexs(indexs, dates)
  pass