import financial_download as FD
from stock_codes_utility import stock_codes_utility as SCU
from stock_basic import *

def stock_basic_finance_download(path_root='../../../data/'):
  FD.download_finance(path_root);
  download_all_stocks_basic(path_root);
  processed_all_stocks_basic(path_root);

if __name__ == '__main__':
  path = '../../../data_finance_basic/'
  stock_basic_finance_download(path)
