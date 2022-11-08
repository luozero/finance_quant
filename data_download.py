import json
import sys, getopt
import datetime
import os
sys.path.append(r'./')
sys.path.append(os.path.abspath('./efinance'))

from ultility.common_def import *
from ultility.common_func import *

from ultility.stock_codes_utility import stock_codes_utility as SCU
from data_set.finance_data.data_download import data_download
from data_set.finance_data.finance_factor_calc import *
from data_set.finance_data.finance_factor_rank import *
from data_set.finance_data.stock_basic import *
from data_set.trade_data.process_daily_trade_data import process_daily_trade_data

#efinance
from data_set.efinance_download.money_flow import *

def download_163(path, path_in, data_type):
    scu = SCU(path, data_type)
    stock_codes = scu.stock_codes_from_table(data_type)
    # stock_codes = ['600000']
    print(stock_codes)
    data_download_1 = data_download(path, path_in, stock_codes, data_type)
    data_download_1.download_data(data_type)

def download_eastmoney_index(path, conf_trade):

  download = money_flow(path)
  download.get_stock_north_index()

  indexs = conf_trade["eastmoney_indexs"]
  blocks = conf_trade["eastmoney_blocks"]
  download.get_index_block_data(indexs, blocks)

def download_eastmoney_stock_data_daily(path):
  download = money_flow(path)
  download.get_stock_margin_short_total()
  download.get_stock_north()
  download.get_stock_north_new()
  download.get_stock_bill()

  download.get_stock_margin_short()
  download.get_stock_big_deal()

def download_money_flow(path, folder):

  path_data = os.path.join(path, folder['money_flow'])
  download = money_flow(path_data)
  download.get_shsz_big_bill()

def download_north_south(path, folder):

  path_data = os.path.join(path, folder['north_south'])
  download = money_flow(path_data)
  download.get_north_south_history()

def download_data(conf):
  
  common_conf = conf['common']
  path = common_conf['path']
  folder = common_conf["folder"]

  download_163_finance_flag = common_conf['download_163_finance_flag']
  download_163_stock_daily_flag = common_conf['download_163_stock_daily_flag']
  download_163_index_daily_flag = common_conf['download_163_index_daily_flag']
  download_eastmoney_index_daily_flag = common_conf['download_eastmoney_index_daily_flag']
  download_eastmoney_stock_daily_flag = common_conf['download_eastmoney_stock_daily_flag']
  download_north_south_flag = common_conf['download_north_south_flag']

  # stock_codes = scu.stock_codes()
  # stock_codes = ['SH600032']

  download_money_flow(path, folder)

  # download all the data
  if download_163_finance_flag == "yes":
    path_finance = os.path.join(path, folder['data_stock'])
    download_163(path, path_finance, TYPE_FINANCE_STOCK)

  if download_163_stock_daily_flag == "yes":
    data_stock = os.path.join(path, folder['data_stock'])
    download_163(path, data_stock, TYPE_STOCK)

  if download_163_index_daily_flag == "yes":
    path_index = os.path.join(path, folder['data_index'])
    download_163(path, path_index, TYPE_INDEX)

  if download_eastmoney_index_daily_flag == "yes":
    path_index = os.path.join(path, folder['data_index'])
    download_eastmoney_index(path_index, conf["trade"])

  if download_eastmoney_stock_daily_flag == "yes":
    path_data = os.path.join(path, folder['data_stock'])
    download_eastmoney_stock_data_daily(path_data)

  if download_north_south_flag == 'yes':
    download_north_south(path, folder)
  

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
  download_data(conf)
