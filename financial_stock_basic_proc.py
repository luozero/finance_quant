import sys
import json
sys.path.append(r'../')

# import ptvsd
# ptvsd.settrace(None, ('0.0.0.0', 12345))

from stock_deeplearning.data_set.finance_data.stock_data_download import download_finance
from stock_deeplearning.data_set.finance_data.stock_basic import *
from stock_deeplearning.data_set.finance_data.financial_factor_calc import *
from stock_deeplearning.data_set.finance_data.financial_factor_rank import *
from stock_deeplearning.data_set.trade_data.process_daily_trade_data import process_daily_trade_data
from stock_deeplearning.ultility.common_def import process_record_dict

def read_config(filename):
  with open(filename, 'r') as f:
    conf = json.load(f)
  return conf

def finance_process(conf):
  
  common_conf = conf['common']
  download_finance = common_conf['download_finance']
  path = common_conf['path']

  finance_conf = conf['finance']
  result_name = finance_conf['result_name']
  dates = finance_conf['dates']
  factors = finance_conf['factors']

  scu = SCU(path)
  stock_codes = scu.stock_codes()
  # stock_codes = ['000001','000002']

  # download all the data
  if download_finance:
    download_finance(path, stock_codes, True)

  # process quarter trade
  daily_trade_data = process_daily_trade_data(path, stock_codes)
  daily_trade_data.trade_data_quarter()

  # need to disable following code when debug
  stock_codes = scu.skip_stock_codes(stock_codes)

  # factors caculate
  stock_factors_calc(path, stock_codes)

  # rank the factor
  financial_factors_rank(path, result_name, stock_codes, dates, factors)

def trade_process(conf):

  common_conf = conf['common']
  download_finance = common_conf['download_finance']
  path = common_conf['path']

  trade_conf = conf['trade']
  trade_ouput_file = trade_conf['trade_ratio_file']


  scu = SCU(path)
  stock_codes = scu.stock_codes()
  # stock_codes = ['000001','000002']

  # download daily trade data
  if download_finance:
    download_finance(path, stock_codes, False)

  # need to disable following code when debug
  stock_codes = scu.skip_stock_codes(stock_codes)

  #process daily trade data
  daily_trade_data = process_daily_trade_data(path, stock_codes)
  daily_trade_data.price_volume_ration(stock_codes, trade_ouput_file)

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
  trade_flag = conf["common"]["trade_flag"]
  
  if trade_flag:
    trade_process(conf)
  else:
    finance_process(conf)
  
