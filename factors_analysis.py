import json
import os
import sys, getopt
import datetime
sys.path.append(os.path.abspath('./efinance'))
# sys.path.append(r'../')

from stock_ai.trade_ratio_ml import trade_ratio_ml
from ultility.common_def import *
from ultility.common_func import *
from ultility.stock_codes_utility import *



def trade_ratio_k_mean(conf, stock_codes, trade_ratio_file, kmean_trade_ratio_file):

  common_conf = conf['common']
  path = common_conf['path']
  folder = common_conf["folder"]

  trade_conf = conf['trade']

  path_in = os.path.join(path, folder['process_trade'])
  path_out = os.path.join(path, folder['process_analyse'])

  n_clusters = trade_conf['n_clusters']


  trade_ratio = trade_ratio_ml(stock_codes, path_in, path_out, trade_ratio_file)
  trade_ratio.kmean(n_clusters, kmean_trade_ratio_file)

def trade_kmean(conf):
  trade_conf = conf['trade']
  common_conf = conf['common']
  path = common_conf['path']
  folder = common_conf["folder"]
  finance_conf = conf['finance']

  # stock analyse
  scu = stock_codes_utility(type_data = CONST_DEF.TYPE_STOCK)
  stock_codes = scu.stock_codes_from_table()
  csv_finance_factor = os.path.join(path, folder['finance_rank'], finance_conf['result_name'])
  pd1 = pd.read_csv(csv_finance_factor, encoding='gbk')
  kmnean_stock_num =  trade_conf['kmnean_stock_num']
  stock_codes = pd1.iloc[1:kmnean_stock_num, 0].apply(lambda x: x[1:])
  trade_ratio_file = trade_conf['stock_trade_ratio_file']
  kmean_trade_ratio_file = trade_conf['stock_kmean_trade_ratio_file']
  trade_ratio_k_mean(conf, stock_codes, trade_ratio_file, kmean_trade_ratio_file)

  #index analyse
  scu = stock_codes_utility(type_data = TYPE_INDEX)
  stock_codes = scu.stock_codes_from_table()
  trade_ratio_file = trade_conf['index_trade_ratio_file']
  kmean_trade_ratio_file = trade_conf['index_kmean_trade_ratio_file']
  trade_ratio_k_mean(conf, stock_codes, trade_ratio_file, kmean_trade_ratio_file)

  #block analyse
  scu = stock_codes_utility()
  stock_codes = scu.block_codes_from_eastmoney()
  trade_ratio_file = trade_conf['block_trade_ratio_file']
  kmean_trade_ratio_file = trade_conf['block_kmean_trade_ratio_file']
  trade_ratio_k_mean(conf, stock_codes, trade_ratio_file, kmean_trade_ratio_file)

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

  conf = common_func.read_config(filename)

  trade_kmean(conf)

