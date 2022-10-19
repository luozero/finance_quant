import sys
import os
sys.path.append(os.path.abspath('../efinance'))
sys.path.append(r'..')


from data_set.east_money.index_block_getter import *

inde_block_data = get_index_block_data('/tmp/finance_data')
inde_block_data.get_data()
