#-*- coding:UTF-8 -*-
'''
Created on 2018��9��24��

@author: ll
'''
import os
import sys, getopt
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
sys.path.append("./finance_data")
from finance_factor_calc import finance_index_dic as FID
from finance_index_rank import finance_index_rank
import  stock_data_download

#-o ../../../data/score/k300 -k 100
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
  path_plot = '../../../data/figure'
  path_score_kmean = outputfile
  stocks = stock_data_download.ts_stock_codes()
  #stocks = ['000001','000002','000004','000005','000006']
  dates = ['2018-06-30']
  if not os.path.exists(path_plot):
      os.makedirs(path_plot)
  #k = 300
  FIR = finance_index_rank(path=path, path_score=path_score, stocks = stocks, dates = dates)
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
  feth_indexs = FIR.fetch_selected_finance_indexs(indexs, dates,path_score_kmean)
  for i in range(0,9):
    plt.figure()
    feth_indexs['2018-06-30'][indexs[i]].hist(bins=1000)
    plt.title(indexs[i])
    plt.savefig(os.path.join(path_plot,indexs[i]))
  plt.show()

  #fecth_indexs = FIR.fetch_selected_finance_indexs(indexs, dates)
  pass