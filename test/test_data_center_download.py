import sys
import os
sys.path.append(os.path.abspath('../efinance'))
sys.path.append(r'..')


from data_set.east_money.east_money_download import *

east_money_data = east_money_download('/home/finance_data/data/index/')
east_money_data.get_stock_north_index()
# east_money_data = east_money_download('/home/finance_data/data/stock/')
# east_money_data.get_stock_north_new()
# east_money_data.get_stock_bill()
# east_money_data.get_stock_big_deal()
