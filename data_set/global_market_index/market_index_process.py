# coding: utf8
'''
Created on 2018��11��4��

@author: ll
'''
import os
from datetime import datetime
import pandas as pd
import pandas_datareader.data as web
import pandas_datareader as pdr
import quandl
import numpy as np
import math
import matplotlib.pyplot as plt
import sys, getopt

class WorldIndexProcess(object):
  '''
  classdocs
  '''
  def __init__(self, path = '../../../data/',days=1):
    self.index_dic = pd.read_csv('./parameter world index.csv', encoding='ANSI')
    self.date_start = start
    self.date_end = end
    self.path_load = os.path.join(path,'world_index','{}.csv')
    path_store = os.path.join(path,'world_index_processed','days_'+str(days))
    self.days = days
    if not os.path.exists(path_store):
      os.makedirs(path_store)
    self.root_path_store = path_store
    self.path_return = os.path.join(path_store,'world_index_processed.csv')
    self.path_select = os.path.join(path_store,'world_index_select.csv')
    self.path_correlate = os.path.join(path_store,'world_index_correlate_'+start.strftime("%Y-%m-%d")+'.csv')
    self.path_store = os.path.join(path_store,'{}.csv')
    
  def raw_return_calc(self, a,str,days):
    data = (a[days:]-a[:-days])/a[:-days]
    data[np.isinf(data)]=0
    data[np.isnan(data)]=0
    data = data.dot(100)
    dict_data = {str:data}
    pd_data = pd.DataFrame(dict_data)
    return pd_data
  def log_return_calc(self, a,str,days):
    data = (np.log(a[days:])-np.log(a[:-days]))
    data[np.isinf(data)]=0
    data[np.isnan(data)]=0
    data = data.dot(100)
    dict_data = {str:data}
    pd_data = pd.DataFrame(dict_data)
    return pd_data
  def world_index_raw_log_return(self):
    pd_processed_index = pd.DataFrame(columns = ['index','name','discription'])
    for index_name in  self.index_dic.iterrows():
      index = index_name[1].loc['index']
      name = index_name[1].loc['name']
      print('load index:', index, 'name:', name)
      path_load = self.path_load.format(name)
      if not os.path.exists(path_load):
        print('this file not exist', path_load)
        exit(-1)
      data = pd.read_csv(path_load)
      if data.shape[0]>self.days:
        close_price = data['Close'].values.squeeze()
        pd_data = self.raw_return_calc(close_price,'raw_return',self.days)
        pd_data1 = self.log_return_calc(close_price,'log_return',self.days)
        pd_data = pd.concat([pd_data, pd_data1], axis=1)
        pd_data.index = data['Date'][self.days:]
        pd_processed_index = pd_processed_index.append(index_name[1])
        path_store = self.path_store.format(name)
        pd_data.to_csv(path_store)
    pd_processed_index.to_csv(self.path_return,index=False)
  
  def world_index_get(self,index,name,start,end):
    print('load index:', index, 'name:', name)
    path = self.path_store.format(name)
    data = pd.read_csv(path)
    data_select = data[data['Date']>=start]
    data_select = data_select[data_select['Date']<=end]
    data_select['Date'] = pd.to_datetime(data_select['Date'])
    pd_data = pd.concat([data_select['Date'],data_select['log_return']],axis=1)
    pd_data.columns = ['Date',name]
    return pd_data
  
  def world_index_load_align(self,start,end):
    if not os.path.exists(self.path_return):
      self.world_index_raw_log_return()
    index_dic = pd.read_csv(self.path_select, encoding='ANSI')
    index_name = index_dic.iloc[0]
    pd_data_merge = self.world_index_get(index_name[0], index_name[1],start,end)
    for index_name in  index_dic.iloc[1:].iterrows():
      index = index_name[1].loc['index']
      name = index_name[1].loc['name']
      print('load index:', index, 'name:', name)
      pd_data = self.world_index_get(index, name,start,end)
      pd_data_merge = pd.merge(pd_data_merge,pd_data,on='Date', how='outer')
    pd_data_merge = pd_data_merge.sort_values("Date",axis=0,ascending=True)
    pd_data_merge = pd_data_merge.fillna(0)
    data_corr = pd_data_merge.iloc[:,1:].corr()
    data_corr.to_csv(self.path_correlate)
    plt.figure()
    pd_data_merge.iloc[:,1:].plot.bar(pd_data_merge['Date'].apply(lambda x:x.strftime("%Y-%m-%d")))
    plt.savefig(self.root_path_store+'world_index')
    
    return pd_data_merge

  def world_index_plot(self):
    if not os.path.exists(self.path_return):
      self.world_index_raw_log_return()
    index_dic = pd.read_csv(self.path_return, encoding='ANSI')
    for index_name in  index_dic.iterrows():
      index = index_name[1].loc['index']
      name = index_name[1].loc['name']
      print('load index:', index, 'name:', name)
      path_store = self.path_store.format(name)
      data = pd.read_csv(path_store)
      plt.figure()
      plt.subplot(211)
      data['raw_return'].hist(bins=100)
      plt.title(name)
      plt.subplot(212)
      data['log_return'].hist(bins=100)
      plt.savefig(self.root_path_store+name.replace('.', ''))
    #plt.show()
#python market_index_process.py -d 10 -s 2015-1-1 -e 2015-10-1
if __name__ == '__main__':

  days = 10
  start = datetime(2017, 1, 1)
  end = datetime.now()
  start = datetime(2007,1,1)
  end = datetime(2007,11,7)
  try:
    opts, args = getopt.getopt(sys.argv[1:],"d:s:e:",["days=","start=","end="])
  except getopt.GetoptError:
    print('wrong input')
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      print('input: -d 5')
      sys.exit()
    elif opt in ("-d", "--days"):
      days = int(arg)
    elif opt in ("-s", "--start"):
      start = arg
      start = datetime.strptime(start, "%Y-%m-%d") 
    elif opt in ("-s", "--start"):
      end = arg
      end = datetime.strptime(end, "%Y-%m-%d")   
       

  path = '../../../data/'
  wip = WorldIndexProcess(path = path,days=days)
  start = start.strftime("%Y-%m-%d")
  end = end.strftime("%Y-%m-%d")
  wip.world_index_load_align(start,end)
  #f = web.DataReader('F', 'iex', start, end)
  #data0 = web.DataReader('000001.SS','yahoo', start, end)  # S&P 500
  
  #dataA = web.DataReader('^GSPC','yahoo', start, end)  # S&P 500
  #dataB = web.DataReader('^IXIC','yahoo', start, end)  # NASDAQ
  
  #dataC = web.DataReader('DJIA','fred')
  #quandl.ApiConfig.api_key = "kg2SPhseiJ7AxRy1oBqn"
  #df = web.DataReader('WIKI/AAPL', 'quandl', '2015-01-01', '2015-01-05')
  print("processed successfully!!!")
 # data_main = data[0]