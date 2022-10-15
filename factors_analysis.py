import json
import os
import sys, getopt
import datetime
# sys.path.append(r'../')

from stock_ai.trade_ratio_ml import trade_ratio_ml
from ultility.common_def import *
from ultility.common_func import *



def trade_ratio_k_mean(conf, data_type):

  common_conf = conf['common']
  path = common_conf['path']
  folder = common_conf["folder"]

  trade_conf = conf['trade']

  if data_type == TYPE_STOCK:
    trade_ratio_file = trade_conf['stock_trade_ratio_file']
    kmean_trade_ratio_file = trade_conf['stock_kmean_trade_ratio_file']
  elif data_type == TYPE_INDEX:
    trade_ratio_file = trade_conf['index_trade_ratio_file']
    kmean_trade_ratio_file = trade_conf['index_kmean_trade_ratio_file']

  path_finance_rank = os.path.join(path, folder['finance_rank'])
  path_in = os.path.join(path, folder['process_trade'])
  path_out = os.path.join(path, folder['process_analyse'])

  n_clusters = trade_conf['n_clusters']
  kmnean_stock_num =  trade_conf['kmnean_stock_num']

  finance_conf = conf['finance']
  finance_factor_rank_file = finance_conf['result_name']

  trade_ratio = trade_ratio_ml(path_finance_rank, path_in, path_out, trade_ratio_file, finance_factor_rank_file, data_type, kmnean_stock_num)
  trade_ratio.kmean(n_clusters, kmean_trade_ratio_file)

# def trade_kmean(conf):


if __name__ == '__main__':

  # default configure file name
  filename = './conf/conf.json'
  # default finance analysis
  trade_flag =  False 
  # tradeflag =  True 
  try:
    opts, args = getopt.getopt(sys.argv[1:], "f:p:t:", ["filename=", "path=", "tradeflag="])
  except getopt.GetoptError:
    print('test.py -o <outputfile>')
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      print('python3  finance_stock_basic_proc.py -f conf.json')
    elif opt in ("-f", "--filename"):
      filename = arg
    elif opt in ("-t", "--tradeflag"):
      trade_flag = True 

  conf = read_config(filename)
  
  trade_ratio_k_mean(conf, TYPE_STOCK)
  trade_ratio_k_mean(conf, TYPE_INDEX)
  
