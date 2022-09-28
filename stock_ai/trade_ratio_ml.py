# coding: utf8
'''
Created on 2018年9月23日

'''
import os

import pandas as pd
import numpy as np

from sklearn.cluster import KMeans
from stock_deeplearning.ultility.common_def import * 


# from sklearn.cluster import DBSCAN
# from sklearn.cluster import spectral_clustering
# from sklearn.cluster import AgglomerativeClustering


class trade_ratio_ml:
  def __init__(self, path = '../../../data/finance_processed', file_trade_ratio='trade_ratio.csv', file_finance_rank='rank.csk', stock_num = 100):

    stock_folder_daily_trade = os.path.join(path, FOLDER_DAILY_TRADE_PROCESSED)
    if not os.path.exists(stock_folder_daily_trade):
      print("pls run trade ratio python to generate file", file_trade_ratio)

    self.daily_trade_ratio_file = stock_folder_daily_trade + '/' + file_trade_ratio
    self.daily_trade_ratio_folder = stock_folder_daily_trade + '/'

    csv_finance_factor = os.path.join(path, FOLDER_RANK, file_finance_rank)
    pd1 = pd.read_csv(csv_finance_factor, encoding='gbk')
    self.stock_codes = pd1.iloc[1:stock_num, 0]

    
  def kmean(self, k = 10, outputfile = 'output.csv'):
    #fecth_indexs = FIR.fetch_selected_financial_indexs(indexs, self.dates)
    #date = '2017-12-31'

    trade_ratio_tmp = pd.read_csv(self.daily_trade_ratio_file, encoding='gbk')

    pd_trade_ratio_filter = pd.DataFrame()
    trade_ratio_tmp1 = trade_ratio_tmp.set_index(trade_ratio_tmp.iloc[:,0])
    for stock_code in self.stock_codes:
      try:
        data = trade_ratio_tmp1.loc[stock_code, :]
        print("used stock code: ", stock_code)
        pd_trade_ratio_filter = pd.concat([pd_trade_ratio_filter, data], axis = 1)
      except:
        print("dismiss stock code: ", stock_code)

    trade_ratio = pd_trade_ratio_filter.T.reset_index(drop=True)

    trade_ratio = trade_ratio.dropna()
    trade_ratio = trade_ratio.replace(np.inf, 0)
    kmeans = KMeans(n_clusters=k, random_state=0).fit(trade_ratio.iloc[:,1:].values)
    labels = kmeans.labels_

    trade_ratio_cluster = pd.concat([trade_ratio, pd.DataFrame(labels, columns=['cluster'])], axis = 1)
    trade_ratio_cluster = trade_ratio_cluster.sort_values(by=['cluster'])
    trade_ratio_cluster.to_csv(self.daily_trade_ratio_folder + outputfile, encoding='gbk', index = False)
    print("store file: ", self.daily_trade_ratio_folder + outputfile)
