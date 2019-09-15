import sys
sys.path.append(r'../')

import stock_deeplearning.data_set.stock_get_finance_data.financial_download  as FD
from stock_deeplearning.data_set.stock_get_finance_data.stock_basic import *


def stock_basic_finance_download(path_root='../../../data/'):
  FD.download_finance(path_root)
  download_all_stocks_basic(path_root)
  processed_all_stocks_basic(path_root)

if __name__ == '__main__':
  path = '../data_finance_basic/'
  stock_basic_finance_download(path)
