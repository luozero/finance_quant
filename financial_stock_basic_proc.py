import sys
import json
sys.path.append(r'../')

from stock_deeplearning.data_set.finance_data.financial_download import download_finance
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

# need to disable following code when debug
  # scu = SCU(path=path_root)
  # stock_codes = scu.stock_codes_remove_no_stock_basic()

  main_financial_data_process(path_root, stock_codes)

def factors_rank(path_root='../data/', filename = 'rank_result', stock_codes = ['000001'],
                dates = ['2018-09-30'], factors = [FID['roe'], FID['roa']]):
  financial_factors_rank(path_root, filename, stock_codes, dates, factors)


if __name__ == '__main__':
  path = '../data_20200516/'
  filename = 'conf.json'
  try:
    opts, args = getopt.getopt(sys.argv[1:], "f:p:", ["filename=", "path="])
  except getopt.GetoptError:
    print('test.py -o <outputfile>')
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      print('test.py -o <outputfile>')
    elif opt in ("-f", "--filename"):
      filename = arg
    elif opt in ("-p", "--path"):
      path = arg
  

  conf = read_config(filename)
  path = conf['path']
  result_name = conf['result_name']
  dates = conf['dates']
  factors = conf['factors']

  # factors = [
  #   # earning capacity
  #   FID['roe'], \
  #   FID['roa'], \
  #   FID['profit_revenue'], \
  #   FID['cash_incr_rate'], \
  #   # FID['profit_cost'],\
  #   # FID['equlity_incr_rate'],\
  #   # grow capacity
  #   FID['revenue_incr_rate'],\
  #   FID['profit_incr_rate'],\
  #   # FID['cash_incr_rate'],\
  #   # FID['asset_incr_rate'],\
  # ]
  # dates = ['2018-09-30', '2018-06-30', '2017-12-31', '2016-12-31', '2015-12-31', '2014-12-31']  # ,'2017-12-31'
  # dates = ['2019-12-31', '2019-09-30', '2019-06-30', '2019-03-31']  # ,'2017-12-31'
  # dates = ['2020-03-31', '2019-12-31', '2019-09-30', '2019-06-30', '2019-03-31']  # ,'2017-12-31'

  

  scu = SCU(path)
  # stock_codes = scu.stock_codes()
  stock_codes = ['000001','000002']

  stock_basic_finance_download(path, stock_codes)

  factors_rank(path, result_name, stock_codes, dates, factors)
