import sys
import os
sys.path.append(os.path.abspath('../efinance'))
sys.path.append(r'..')


from data_set.east_money.east_money_download import *

east_money_data = east_money_download('/tmp/finance_data')
east_money_data.get_index_block_data(indexs = ['sh', 'sz', 'sh_sz', 'cn'], blocks = [])
