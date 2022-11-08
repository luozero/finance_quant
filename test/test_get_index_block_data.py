import sys
import os
sys.path.append(os.path.abspath('../efinance'))
sys.path.append(r'..')


from data_set.efinance_download.money_flow import *

east_money_data = money_flow('/tmp/finance_data')
east_money_data.get_index_block_data(indexs = ['sh', 'sz', 'sh_sz', 'cn'], blocks = [])
