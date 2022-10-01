# coding: utf8
import pandas as pd
import os
import json
from stock_deeplearning.ultility.common_def import * 

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

  def read_date(self):
    if not os.path.exists(self.path_file):
      return 0
    with open(self.path_file) as f:
        summary = json.load(f)
    index = summary['date']
    return index

  def write_date(self, date):
    with open(self.path_file, 'w') as f:
      summary = dict(
              date = date
      )
      json.dump(summary, f)

  def write_data(self, key1, key2, value):

    process_record_dict = {}
    if os.path.exists(self.path_file):
      with open(self.path_file) as f:
          process_record_dict = json.load(f)
      
      process_record_dict[key1].update({key2: value})
    else:
      process_record_dict = {key1: {key2: value}}

    with open(self.path_file, 'w') as f:
      json_data = process_record_dict
      json.dump(json_data, f)
  
  def read_data(self, key1, key2):

    if not os.path.exists(self.path_file):
      print(self.path_file + "is not exist!!!")
      return 0
    with open(self.path_file) as f:
        json_data = json.load(f)
    
    try:
      data = json_data[key1][key2]
    except:
      data = 0

    return data

  def write_skip_stock(self, stock):
    # add s
    sstock = 's' + stock
    if os.path.exists(self.path_stock_rec):
      pd_skip = pd.read_csv(self.path_stock_rec)
      pd_skip1 = pd.DataFrame([sstock],columns=['stock'])
      pd_skip = pd_skip.append(pd_skip1,ignore_index=True)
      # pd_skip = pd_skip.concat(pd_skip1,ignore_index=True)
    else:
      pd_skip = pd.DataFrame([sstock],columns=['stock'])
    pd_skip.to_csv(self.path_stock_rec, encoding='gbk', index = False)
    
  def read_skip_stock(self):

    if os.path.exists(self.path_stock_rec):
      data = pd.read_csv(self.path_stock_rec, encoding='gbk')
      # remove s
      data = data.applymap(lambda x: x[1:])
      return data.loc[:,'stock']
    return pd.DataFrame()
  
  def write_stock(self,stock):
    pd_skip = pd.DataFrame(stock,columns=['stock'])
    pd_skip.to_csv(self.path_stock_rec, index = False)
    
  def read_stock(self):
    data = pd.read_csv(self.path_stock_rec)
    return data.loc[:,'stock']