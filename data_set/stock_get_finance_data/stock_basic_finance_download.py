import financial_download as FD
from stock_codes_utility import stock_codes_utility as SCU

def stoc_basic_finance_download(path_root = '../../../data/'):

  FD.download_finance(path_root);
  SCU.download_all_stocks_basic(path_root);
  SCU.processed_all_stocks_basic(path_root);

if __name__ == '__main__':
  path = '../../../data_finance_basic/'
  stoc_basic_finance_download(path)
