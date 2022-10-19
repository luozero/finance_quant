import os
import sys

import efinance as ef

class get_index_block_data:
  def __init__(self, path, indexs = ['sh', 'sz', 'sh_sz', 'cn'], blocks = ['indurstry', 'concept', 'province']):
    
    self.path = path
    if not os.path.exists(path):
      os.makedirs(path)
    self.blocks = blocks
    self.indexs = indexs

    self.push2_98_getter = ef.stock.push2_98_getter.push2_98()

  def get_data_common(self, codes, path):

    if not os.path.exists(path):
      os.makedirs(path)
    for code in codes:
      print("download code", code)
      data = ef.stock.get_quote_history(code)
      file = os.path.join(path, code + '.csv')
      data.to_csv(file, encoding='gbk')
     
    
  def get_data(self):
      
    for block in self.blocks:
      code_names = self.push2_98_getter.get_block_codes(block)
      self.get_data_common(code_names.loc[:, 'code'].values, os.path.join(self.path, block))

    for index in self.indexs:
      code_names = self.push2_98_getter.get_index_codes(index)
      self.get_data_common(code_names.loc[:, 'code'].values, os.path.join(self.path, index))