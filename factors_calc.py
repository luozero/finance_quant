import json
import sys, getopt
import datetime

from ultility.common_def import *
sys.path.append(r'../')

# import ptvsd
# ptvsd.settrace(None, ('0.0.0.0', 12345))

from ultility.stock_codes_utility import stock_codes_utility as SCU
from data_set.finance_data.data_download import data_download
from data_set.finance_data.finance_factor_calc import *
from data_set.finance_data.finance_factor_rank import *
from data_set.finance_data.stock_basic import *
from data_set.trade_data.process_daily_trade_data import process_daily_trade_data

def read_config(filename):
  with open(filename, 'r') as f:
    conf = json.load(f)
  return conf

def finance_factor_process(conf):
  
  common_conf = conf['common']
  download = common_conf['download']
  folder = common_conf["folder"]


  path = common_conf['path']
  path_finance = os.path.join(path, folder['data_finance'])
  path_factor = os.path.join(path, folder["finance_factors"])
  path_rank = os.path.join(path, folder["finance_rank"])


  result_name = finance_conf['result_name']

  finance_conf = conf['finance']
  dates = finance_conf['dates']
  factors = finance_conf['factors']

  data_type = 'finance_stock_data'
  scu = SCU(path)
  # stock_codes = scu.stock_codes()
  stock_codes = scu.stock_codes_from_table(data_type)
  print(stock_codes)
  # stock_codes = ['SH600032']

  # process quarter trade
  daily_trade_data = process_daily_trade_data(path, path_finance, path_finance, stock_codes, data_type)
  daily_trade_data.trade_data_quarter()

  # need to disable following code when debug
  stock_codes = scu.skip_stock_codes(stock_codes)

  # factors caculate
  ffc = finance_factor_calc(path, path_finance, path_factor)
  ffc.stock_factors_calc(stock_codes)

  # rank the factor
  finance_factors_rank(path_factor, path_rank, result_name, stock_codes, dates, factors)

def daily_trade_process(conf):

  common_conf = conf['common']
  folder = common_conf["folder"]
  path = common_conf['path']
  trade_conf = conf['trade']

  finance_163_daily_trade_factor = trade_conf['finance_163_daily_trade_factor']
  stock_163_daily_trade_factor = trade_conf['stock_163_daily_trade_factor']
  index_163_daily_trade_factor = trade_conf['index_163_daily_trade_factor']

  if finance_163_daily_trade_factor == 'yes':
    finance_factor_process(conf)

  if stock_163_daily_trade_factor == 'yes':
    path_in = os.path.join(path, folder['data_stock'])
    path_out = os.path.join(path, folder['process_trade'])
    trade_ouput_file = trade_conf['stock_trade_ratio_file']
    data_type = TYPE_STOCK
    scu = SCU(path, data_type)
    stock_codes = scu.stock_codes_from_table(data_type)
    # stock_codes = ['SZ301213', 'SH600519']
    # need to disable following code when debug
    stock_codes = scu.skip_stock_codes(stock_codes)
    #process daily trade data
    daily_trade_data = process_daily_trade_data(path, path_in, path_out, stock_codes, data_type)
    daily_trade_data.price_volume_ratio(stock_codes, trade_ouput_file)

  if index_163_daily_trade_factor == 'yes':
    path_in = os.path.join(path, folder['data_index'])
    path_out = os.path.join(path, folder['process_trade'])
    trade_ouput_file = trade_conf['index_trade_ratio_file']
    data_type = TYPE_INDEX
    scu = SCU(path, data_type)
    stock_codes = scu.stock_codes_from_table(data_type)
    #process daily trade data
    daily_trade_data = process_daily_trade_data(path, path_in, path_out, stock_codes, data_type)
    daily_trade_data.price_volume_ratio(stock_codes, trade_ouput_file)


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

  daily_trade_process(conf)

