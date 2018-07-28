#  Copyright 2016 The TensorFlow Authors. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import pandas as pd
from apt.utils import get_maintenance_end_date
from oauthlib.uri_validate import path
import stock_data
from enum import Enum
#from stock_data.stock_process_day_data.loadstore import data
"""Model training for Iris data set using Validation Monitor."""

#from __future__ import absolute_import
#from __future__ import division
#from __future__ import print_function

import os

import numpy as np
import tensorflow as tf

import sys
sys.path.append("../stock_data/stock_process_day_data")
import loadstore

tf.logging.set_verbosity(tf.logging.INFO)

class ProcessDataType(Enum):
  train = 1
  verify = 2
  test = 3

def get_data_stocks(load_store, stock_codes, start_date, end_date, verify_days, test_days, proc_days):
  stocks_train_data = {};
  stocks_verify_data = {};
  stocks_test_data = {};
  for stock in stock_codes:
    stock_data = load_store.load_processing_data_with_date(stock, start_date, end_date)
    stock_data = stock_data.iloc[::-1,:]
    stock_data.pop('date')
    stock_data.index = range(stock_data.shape[0])
    #test
    
    try:
      stocks_test_data[stock] = stock_data.iloc[range(test_days+proc_days)]
      stocks_test_data[stock].index = range(stocks_test_data[stock].shape[0])
    except IndexError:
      print('test data len is', test_days+proc_days, 
            'but the actual data len is',stock_data.shape[0])
      return
    #verify
    
    try:
      stocks_verify_data[stock] = stock_data.iloc[range(test_days, \
                                                   test_days+verify_days+proc_days)]
      stocks_verify_data[stock].index = range(stocks_verify_data[stock].shape[0])
    except IndexError:
      print('verify data len is', verify_days+proc_days, \
            'but the actual data len is',stock_data.shape[0]-test_days-proc_days)
      return

    #train
    try:
      stocks_train_data[stock] = stock_data.iloc[range(test_days+verify_days, \
                                                  stock_data.shape[0])]
      stocks_train_data[stock].index = range(stocks_train_data[stock].shape[0])
    except IndexError:
      print('train data len is', verify_days+proc_days, \
            'but the actual data len is',stock_data.shape[0]-test_days-verify_days)
      return
  return pd.Panel(stocks_test_data), pd.Panel(stocks_verify_data),\
    pd.Panel(stocks_train_data)

class StockTradeData(object):
  def __init__(self, stock_codes, path_data='../stock_data/stockdata/stocktradedata', 
               path_result='../stock_data/stockdata/pctdata', start_date='2014-01-01',
                end_date='2014-03-16', proc_days=15,verify_days=20,test_days=20):
    self.stock_codes = stock_codes
    self.path = path
    self.start_date = start_date
    self.end_date = end_date
    self.proc_days = proc_days 
    #self.load_store = loadstore.use(export='csv',path_data='../easyhistory/history/',path_result='/income/',dtype='D')
    self.load_store = loadstore.use(export='csv', path_data=path_data, path_result=path_result, dtype='D')
    
    self.train_data_index  = 0
    self.verify_data_index  = 0
    self.test_data_index  = 0
    self.verify_days = verify_days
    self.test_days = test_days
    self.stocks_test_data, self.stocks_verify_data, self.stocks_train_data = \
    get_data_stocks(self.load_store, stock_codes, start_date, end_date,verify_days,test_days,proc_days)
  
  def reset_data_index(self,data_type):
    if(ProcessDataType.train == data_type):
      self.train_data_index = 0
    elif(ProcessDataType.verify == data_type):
      self.verify_data_index = 0
    else:
      self.test_data_index = 0
      
  def get_data_index(self,data_type):
    if(ProcessDataType.train == data_type):
      return self.train_data_index
    elif(ProcessDataType.verify == data_type):
      return self.verify_data_index
    else:
      return self.test_data_index
    
  def add_data_index(self,data_type):
    if(ProcessDataType.train == data_type):
      self.train_data_index = self.train_data_index+1
    elif(ProcessDataType.verify == data_type):
      self.verify_data_index = self.verify_data_index+1
    else:
      self.test_data_index = self.test_data_index+1
  
  def input_func(self, train_stock, batch_size, future_day, data_type):
    
    if data_type == ProcessDataType.train:
      data_stocks = self.stocks_train_data
    elif data_type == ProcessDataType.verify:
      data_stocks = self.stocks_verify_data
    else:
      data_stocks = self.stocks_test_data

    #data_stocks = data_stocks.iloc[:,::-1,:]
    (x,y,z) = data_stocks.shape
    data_index = self.data_index 
    if ((data_index+1)*self.proc_days+batch_size+future_day)>y:
      if data_index == 0:
        print("need data lenght is",((data_index+1)*self.proc_days+batch_size+future_day),
        "but acctual data length is", y)
      self.reset_data_index(data_type)
      data_index = 0
    else:
      data_index = self.get_data_index(data_type)
      self.add_data_index(data_type)
      
    output_index = list(range(data_index*self.proc_days,data_index*self.proc_days+batch_size))
    closed_price = data_stocks[train_stock,output_index,'close']
    
    input_data = pd.DataFrame()
    for i in range(0,batch_size):
      input_index = list(range(data_index*self.proc_days+future_day+i,
                               (data_index+1)*self.proc_days+batch_size+future_day+i))
      data_select = data_stocks[:,input_index,:]
      data_sel_array = data_select.values
      input_data[i]= data_sel_array.ravel()
    return closed_price, input_data

if __name__ == "__main__":
  #tf.app.run()
  stock_trade_data = StockTradeData(stock_codes=['000001','000002'],proc_days=15,verify_days=10,test_days=10)
  stock_trade_data.reset_data_index()
  inputdata, price = stock_trade_data.input_func('000001', 2, 1, ProcessDataType.train)
