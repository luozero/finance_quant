import json
import sys, getopt
sys.path.append(r'../')

from stock_deeplearning.stock_ai.trade_ratio_ml import trade_ratio_ml

def read_config(filename):
  with open(filename, 'r') as f:
    conf = json.load(f)
  return conf

def trade_ratio_k_mean(conf):

  common_conf = conf['common']
  path = common_conf['path']

  trade_conf = conf['trade']
  trade_ratio_file = trade_conf['trade_ratio_file']
  kmean_trade_ratio_file = trade_conf['kmean_trade_ratio_file']
  n_clusters = trade_conf['n_clusters']
  kmnean_stock_num =  trade_conf['kmnean_stock_num']

  finance_conf = conf['finance']
  finance_factor_rank_file = finance_conf['result_name']

  trade_ratio = trade_ratio_ml(path, trade_ratio_file, finance_factor_rank_file, kmnean_stock_num)
  trade_ratio.kmean(n_clusters, kmean_trade_ratio_file)

# def trade_kmean(conf):


if __name__ == '__main__':

  # default configure file name
  filename = 'conf.json'
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
      print('python3  financial_stock_basic_proc.py -f conf.json')
    elif opt in ("-f", "--filename"):
      filename = arg
    elif opt in ("-t", "--tradeflag"):
      trade_flag = True 

  conf = read_config(filename)
  
  trade_ratio_k_mean(conf)
  
