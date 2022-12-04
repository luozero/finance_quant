import json
import sys, getopt, os
import datetime
sys.path.append(r'../')
sys.path.append(os.path.abspath('./efinance'))

from ultility.common_def import *
from ultility.common_func import *

from ultility.stock_codes_utility import stock_codes_utility as SCU
from data_set.finance_data.data_download import data_download
from data_set.finance_data.finance_factor_calc import *
from data_set.finance_data.finance_factor_rank import *
from data_set.process_data.process_daily_trade import process_daily_trade
from data_set.process_data.process_detailed_trade import *

def finance_factor_process(conf):
  
  common_conf = conf['common']
  folder = common_conf["folder"]
  path = common_conf['path']
  path_stock = os.path.join(path, folder['data_stock'])
  path_rank = os.path.join(path, folder["finance_rank"])

  finance_conf = conf['finance']
  result_name = finance_conf['result_name']
  dates = finance_conf['dates']
  factors = finance_conf['factors']

  scu = SCU(path, CONST_DEF.TYPE_STOCK)
  # stock_codes = scu.stock_codes()
  stock_codes = scu.stock_codes_from_table()
  print(stock_codes)
  # stock_codes = ['600032']

  # process quarter trade
  daily_trade_data = process_daily_trade(path, path_stock, path_stock)
  daily_trade_data.trade_data_quarter(stock_codes)

  # need to disable following code when debug
  stock_codes = scu.skip_stock_codes(stock_codes)

  # factors caculate
  ffc = finance_factor_calc(path, path_stock, path_stock)
  ffc.stock_factors_calc(stock_codes)

  # rank the factor
  finance_factors_rank(path_stock, path_rank, result_name, stock_codes, dates, factors)

def daily_stock_trade_process(path, folder_in, folder_out, trade_ouput_file, codes_names):
  path_in = os.path.join(path, folder_in)
  path_out = os.path.join(path, folder_out)
  # stock_codes = ['002830']
  # need to disable following code when debug
  # stock_codes = scu.skip_stock_codes(stock_codes)
  #process daily trade data
  daily_trade_data = process_daily_trade(path, path_in, path_out)
  daily_trade_data.index_price_volume_ratio(codes_names, trade_ouput_file)

def detailed_trade_process(path, folder_in, folder_out, data_type):

  path_in = os.path.join(path, folder_in)
  path_out = os.path.join(path, folder_out)
  scu = SCU(path, data_type)
  stock_codes = scu.stock_codes_from_table()
  # stock_codes = ['000001']
  # stock_codes = ['002830']

  detailed_trade_process = detailed_trade(path, path_in, path_out)
  detailed_trade_process.statistic_detailed_bills(stock_codes)

def daily_trade_process(conf):

  common_conf = conf['common']
  folder = common_conf["folder"]
  path = common_conf['path']
  trade_conf = conf['trade']

  finance_163_daily_trade_factor = trade_conf['finance_163_daily_trade_factor']
  stock_163_daily_trade_factor = trade_conf['stock_163_daily_trade_factor']
  stock_163_detailed_trade_factor = trade_conf['stock_163_detailed_trade_factor']
  index_163_daily_trade_factor = trade_conf['index_163_daily_trade_factor']
  block_daily_trade_factor = trade_conf['block_daily_trade_factor']

  if finance_163_daily_trade_factor == 'yes':
    finance_factor_process(conf)

  if stock_163_daily_trade_factor == 'yes':
    scu = SCU(path, CONST_DEF.TYPE_STOCK)
    codes_names = scu.stock_codes_names_from_table()
    daily_stock_trade_process(path, folder['data_stock'], folder['process_trade'], trade_conf['stock_trade_ratio_file'], codes_names)

  if block_daily_trade_factor == 'yes':
    scu = SCU(path, CONST_DEF.TYPE_INDEX)
    codes_names = scu.block_codes_names_from_eastmoney('indurstry')
    daily_stock_trade_process(path, folder['data_index'], folder['process_trade'], trade_conf['block_trade_ratio_file'], codes_names)

  if stock_163_detailed_trade_factor == "yes":
    folder_in = folder['data_detailed_stock']
    folder_out = folder['data_stock']
    detailed_trade_process(path, folder_in, folder_out, CONST_DEF.TYPE_DETAILED_STOCK)


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

  daily_trade_process(conf)

