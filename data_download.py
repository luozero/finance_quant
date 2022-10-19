import json
import sys, getopt
import datetime

from ultility.common_def import *
from ultility.common_func import *
sys.path.append(r'../')
sys.path.append(os.path.abspath('./efinance'))

from ultility.stock_codes_utility import stock_codes_utility as SCU
from data_set.finance_data.data_download import data_download
from data_set.finance_data.finance_factor_calc import *
from data_set.finance_data.finance_factor_rank import *
from data_set.finance_data.stock_basic import *
from data_set.trade_data.process_daily_trade_data import process_daily_trade_data

#efinance
from data_set.east_money.index_block_getter import *

def download_163(path, path_in, data_type):
    scu = SCU(path)
    stock_codes = scu.stock_codes_from_table(data_type)
    print(stock_codes)
    data_download_1 = data_download(path_in, stock_codes, data_type)
    data_download_1.download_data(data_type)

def download_eastmoney(path, conf_trade):
  indexs = conf_trade["eastmoney_indexs"]
  blocks = conf_trade["eastmoney_blocks"]
  inde_block_data = get_index_block_data(path)
  inde_block_data.get_data()

def download_163_data(conf):
  
  common_conf = conf['common']
  path = common_conf['path']
  folder = common_conf["folder"]

  download_163_finance = common_conf['download_163_finance']
  download_163_stock_trade = common_conf['download_163_stock_trade']
  download_163_index_trade = common_conf['download_163_index_trade']
  download_eastmoney_index_block_trade = common_conf['download_eastmoney_index_block_trade']

  # stock_codes = scu.stock_codes()
  # stock_codes = ['SH600032']

  # download all the data
  if download_163_finance == "yes":
    path_finance = os.path.join(path, folder['data_finance'])
    download_163(path, path_finance, TYPE_FINANCE_STOCK)

  if download_163_stock_trade == "yes":
    path_trade = os.path.join(path, folder['data_stock'])
    download_163(path, path_trade, TYPE_STOCK)

  if download_163_index_trade == "yes":
    path_index = os.path.join(path, folder['data_index'])
    download_163(path, path_index, TYPE_INDEX)

  if download_eastmoney_index_block_trade == "yes":
    path_index = os.path.join(path, folder['data_index'])
    download_eastmoney(path_index, conf["trade"])

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
  download_163_data(conf)