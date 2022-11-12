# coding: utf8
'''
Created on 2018年9月23日

'''
import os

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans

from ultility.common_def import * 
from ultility.common_func import * 

# from sklearn.cluster import DBSCAN
# from sklearn.cluster import spectral_clustering
# from sklearn.cluster import AgglomerativeClustering

class trade_ratio_ml:
  def __init__(self, stock_codes = ['000001'], path_in = 'path_in', path_out = 'path_out', file_trade_ratio='trade_ratio.csv'):

    path_out = os.path.join(path_out, common_func.get_today_date())
    if not os.path.exists(path_out):
      print("pls run trade ratio python to generate file", file_trade_ratio)
      os.makedirs(path_out)
    self.path_out = path_out

    if not os.path.exists(path_in):
      print("pls run trade ratio python to generate file", file_trade_ratio)
    daily_trade_csv = os.path.join(path_in, file_trade_ratio)
    trade_ratio = pd.read_csv(daily_trade_csv, encoding='gbk')

    pd_trade_ratio_filter = pd.DataFrame()
    trade_ratio_tmp1 = trade_ratio.set_index(trade_ratio.iloc[:,0])
    for stock_code in stock_codes:
      try:
        data = trade_ratio_tmp1.loc["'" + stock_code, :]
        print("used stock code: ", stock_code)
        pd_trade_ratio_filter = pd.concat([pd_trade_ratio_filter, data], axis = 1)
      except:
        print("dismiss stock code: ", stock_code)
    trade_ratio = pd_trade_ratio_filter.T.reset_index(drop=True)

    trade_ratio = trade_ratio.dropna()
    trade_ratio = trade_ratio.replace(np.inf, 0)
    self.trade_ratio = trade_ratio

  def kmean(self, k = 10, outputfile = 'output.csv'):

    trade_ratio = self.trade_ratio

    kmeans = KMeans(n_clusters=k, random_state=0).fit(trade_ratio.iloc[:,2:].values)
    labels = kmeans.labels_

    trade_ratio_cluster = pd.concat([trade_ratio, pd.DataFrame(labels, columns=['cluster'])], axis = 1)
    trade_ratio_cluster = trade_ratio_cluster.sort_values(by=['cluster'])
    outputfile = os.path.join(self.path_out, outputfile)
    trade_ratio_cluster.to_csv(outputfile, encoding='gbk', index = False)
    print("store file: ", outputfile)
