# coding: utf8
'''
Created on 2018��11��4��

@author: ll
'''
import os
import datetime
import pandas as pd
import pandas_datareader.data as web
import pandas_datareader as pdr
import quandl

class WorldIndexDownload(object):
  '''
  classdocs
  '''
  def __init__(self, path = '../../../data/world_index',start='2015-01-01',end='2015-01-05'):
    if not os.path.exists(path):
            os.makedirs(path)
    self.index_dic = pd.read_csv('./parameter world index.csv', encoding='ANSI')
    self.date_start = start
    self.date_end = end
    self.path = os.path.join(path,'{}.csv')
  def download_world_index(self):
    for index_name in  self.index_dic.iterrows():
      index = index_name[1].loc['index']
      name = index_name[1].loc['name']
      print('download index:', index, 'name:', name)
      path = self.path.format(name)
      data = web.DataReader(index,'yahoo', start, end,retry_count=300)  # S&P 500
      print('successfully download index:', index, 'name:', name)
      data.to_csv(path)
      
if __name__ == '__main__':

  start = datetime.datetime(2000, 1, 1)
  end = datetime.datetime.now()
  path = '../../../data/world_index'
  wid = WorldIndexDownload(path = path, start = start, end = end)
  wid.download_world_index()
  #f = web.DataReader('F', 'iex', start, end)
  #data0 = web.DataReader('000001.SS','yahoo', start, end)  # S&P 500
  
  #dataA = web.DataReader('^GSPC','yahoo', start, end)  # S&P 500
  #dataB = web.DataReader('^IXIC','yahoo', start, end)  # NASDAQ
  
  #dataC = web.DataReader('DJIA','fred')
  #quandl.ApiConfig.api_key = "kg2SPhseiJ7AxRy1oBqn"
  #df = web.DataReader('WIKI/AAPL', 'quandl', '2015-01-01', '2015-01-05')
  print("processed successfully!!!")
 # data_main = data[0]