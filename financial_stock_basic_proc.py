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

def stock_basic_finance_download(path_root='../data/', stock_codes = ['000001']):

  download_finance(path_root, stock_codes)

  daily_trade_data = process_daily_trade_data(path_root, stock_codes)
  daily_trade_data.processe_daily_trade_data_quarter()

if __name__ == '__main__':

  # default configure file name
  filename = 'conf.json'
  try:
    opts, args = getopt.getopt(sys.argv[1:], "f:p:", ["filename=", "path="])
  except getopt.GetoptError:
    print('test.py -o <outputfile>')
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      print('python3  financial_stock_basic_proc.py -f conf.json')
    elif opt in ("-f", "--filename"):
      filename = arg
  

  conf = read_config(filename)
  path = conf['path']
  result_name = conf['result_name']
  dates = conf['dates']
  factors = conf['factors']

  scu = SCU(path)
  stock_codes = scu.stock_codes()
  # stock_codes = ['000001','000002']

  # download all the data
  stock_basic_finance_download(path, stock_codes)

  # need to disable following code when debug
  stock_codes = scu.skip_stock_codes(stock_codes)

  # factors caculate
  stock_factors_calc(path, stock_codes)

  # rank the factor
  financial_factors_rank(path, result_name, stock_codes, dates, factors)
