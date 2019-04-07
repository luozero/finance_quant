# coding: utf8
import pandas as pd
import os
import json
class download_record:
  def __init__(self,path='../../../data/',record='rec.json', skip = 'skip_stock.csv'):
    self.path_file = os.path.join(path,record)
    self.path_stock_rec = os.path.join(path,skip)
    '''
    classdocs
    '''
  def read_index(self):
    if not os.path.exists(self.path_file):
      return 0
    with open(self.path_file) as f:
        summary = json.load(f)
    index = summary['index']
    return index

  def write_index(self, index):
    with open(self.path_file, 'w') as f:
      summary = dict(
              index = index
      )
      json.dump(summary, f)

  def write_skip_stock(self,stock):
    if os.path.exists(self.path_stock_rec):
      pd_skip = pd.read_csv(self.path_stock_rec)
      pd_skip1 = pd.DataFrame([stock],columns=['stock'])
      pd_skip = pd_skip.append(pd_skip1,ignore_index=True)
    else:
      pd_skip = pd.DataFrame([stock],columns=['stock'])
    pd_skip.to_csv(self.path_stock_rec, index = False)
    
  def read_skip_stock(self):
    if os.path.exists(self.path_stock_re):
      data = pd.read_csv(self.path_stock_rec)
      return data.loc[:,'stock']
    else:
      return False
  
  def write_stock(self,stock):
    pd_skip = pd.DataFrame(stock,columns=['stock'])
    pd_skip.to_csv(self.path_stock_rec, index = False)
    
  def read_stock(self):
    data = pd.read_csv(self.path_stock_rec)
    return data.loc[:,'stock']
    