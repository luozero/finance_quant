import sys
import os
sys.path.append(os.path.abspath('../efinance'))
sys.path.append(r'../')
sys.path.append(r'./')

from data_set.process_data.process_detailed_trade import *

path = '/home/finance_data'
path_out = '/home/finance_data/data/stock'
path_in = '/home/finance_data/data/detailed/stock'
stock_codes = ['000001']

detailed_trade = detailed_trade(path, path_in, path_out)
detailed_trade.statistic_detailed_bills(stock_codes)