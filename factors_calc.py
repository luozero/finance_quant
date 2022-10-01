import json
import sys, getopt

from ultility.common_def import *
sys.path.append(r'../')

# import ptvsd
# ptvsd.settrace(None, ('0.0.0.0', 12345))

from ultility.stock_codes_utility import stock_codes_utility as SCU
from data_set.finance_data.data_download import data_download
from data_set.finance_data.stock_basic import *
from data_set.trade_data.process_daily_trade_data import process_daily_trade_data

def read_config(filename):
  with open(filename, 'r') as f:
    conf = json.load(f)
  return conf

def finance_process(conf):
  
  common_conf = conf['common']
  data_type = common_conf['data_type']
  path = common_conf['path']

  finance_conf = conf['finance']
  result_name = finance_conf['result_name']
  dates = finance_conf['dates']
  factors = finance_conf['factors']

  scu = SCU(path)
  stock_codes = scu.stock_codes()
  # stock_codes = ['000001','000002']

  # download all the data
  data_download_1 = data_download(path, stock_codes)
  data_download_1.download_data(data_type)

  # process quarter trade
  daily_trade_data = process_daily_trade_data(path, stock_codes, data_type)
  daily_trade_data.trade_data_quarter()

  # need to disable following code when debug
  stock_codes = scu.skip_stock_codes(stock_codes)

  # factors caculate
  stock_factors_calc(path, stock_codes)

  # rank the factor
  financial_factors_rank(path, result_name, stock_codes, dates, factors)

def trade_process(conf):

  common_conf = conf['common']
  data_type = common_conf['data_type']
  download = common_conf['download']
  path = common_conf['path']

  trade_conf = conf['trade']

  if data_type == TYPE_STOCK:
    trade_ouput_file = trade_conf['stock_trade_ratio_file']
  elif data_type == TYPE_INDEX:
    trade_ouput_file = trade_conf['index_trade_ratio_file']


  scu = SCU(path)
  # stock_codes = scu.stock_codes()
  stock_codes = scu.stock_codes_from_table(data_type)
  # stock_codes = ['000001','000002']

  # download daily trade data

  data_download_1 = data_download(path, stock_codes)
  if download == "yes":
    data_download_1.download_data(data_type)

  # need to disable following code when debug
  stock_codes = scu.skip_stock_codes(stock_codes)

  #process daily trade data
  daily_trade_data = process_daily_trade_data(path, stock_codes, data_type)
  daily_trade_data.price_volume_ratio(stock_codes, trade_ouput_file)

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
  common_conf = conf['common']
  data_type = common_conf['data_type']
  
  if data_type == TYPE_FINANCE_STOCK:
    finance_process(conf)
  elif data_type == TYPE_INDEX or data_type == TYPE_STOCK:
    trade_process(conf)
  else:
    print('do not support this data type: ', data_type)
  
