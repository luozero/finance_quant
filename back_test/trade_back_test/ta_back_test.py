'''
Created on Aug 5, 2018

@author: root
'''
from . import load
from . import conf

import time
from multiprocessing.pool import ThreadPool
import matplotlib.pyplot as plt
#from . import conf
#from . import strategyVP

#import load
#import conf
import pandas as pd
import numpy
import talib
from talib.abstract import *
from tushare.util.formula import BOLL

class ta_back_test_withdate:
    def __init__(self, path='../../easyhistory/history/', path_income='../income/', suite='defaults'):
        self.load = load.use(export='csv', path=path, path_income=path_income, dtype='D')
        confpara = conf.load_conf('trade_back_test.conf')
        config = dict(confpara[suite])
        self.stock_codes = config['stock_codes'].split(',')
        self.date_start= config['datestart']
        self.date_end= config['dateend']
        
    def trade_back_test_thread(self):
        #stock_codes = self.load.update_stock_codes
        stock_codes = self.stock_codes
       # date_start = self.date_start
       # date_end = self.date_end
        #stock_codes = {'159942','600000', '002379','600519'}
        pool = ThreadPool(1)
        pool.map(self.ta_back_test_processing, stock_codes)
        #self.processing(stock_codes)
        
    def ta_back_test_data(self,stock_code):
        data = self.load.read(stock_code)
        
        data_temp = talib.MACD(data['close'],16,26,9)
        macd_data = pd.DataFrame()
        macd_data['DIF'] = data_temp[0]
        macd_data['DEA'] = data_temp[1]
        macd_data['MACD'] = data_temp[2]
        macd_data.index = data['date']
        
        data_temp = talib.BBANDS(data['close'],26)
        boll_data = pd.DataFrame()
        boll_data['upperband'] = data_temp[0]
        boll_data['middleband'] = data_temp[1]
        boll_data['lowerband'] = data_temp[2]
        boll_data.index = data['date']
        
        #k_data, d_data= talib.STOCHF(data['high'], data['low'], data['close'], fastk_period=9, fastd_period=3, fastd_matype=0)
        k_data, d_data = talib.STOCH(data['high'], data['low'], data['close'], fastk_period=9, slowk_period=3, slowk_matype=0, 
                                     slowd_period=3, slowd_matype=0)
        kd_data = pd.DataFrame()
        kd_data['K'] = k_data
        kd_data['D'] = d_data
        kd_data.index = data['date']
        return (macd_data,boll_data,kd_data)
      
    def load_volume_price_date(self,stock_code,date_start,date_end):
      data = self.load.read_with_date(stock_code,date_start,date_end)
      data_factor = 1#data['factor'].max()
      data_price = data['close']
      data_volume = data['volume']/data_factor
      data_price = data_price/data_factor
      data_date = data['date']
      return (data_volume,data_price,data_date)
        
    def ta_back_test_processing(self, stock_code):
 
        macd_data,boll_data,kdj_data = self.ta_back_test_data(stock_code)
        date_start = self.date_start
        date_end = self.date_end
        #print('load start----------------',stock_code)
        volume, price, date = self.load_volume_price_date(stock_code,date_start,date_end)
        income_total = 0
        start_time = 0
        length = len(volume)
        
        state = 'BOTTOM'
        cnt = 0.000001
        for i in range(start_time,length-1):
            if state == 'BOTTOM':
                #buy_rate_flag = self.strategy.process_daily_limit(price, i, self.daily_limit_rate)

                if macd_data['MACD'][date[i]]<0 and macd_data['MACD'][date[i+1]]>0:
                    state = 'HOLD'
                    buy_price = price[i]
                    buy_date = date[i]
            elif state == 'HOLD':
                if kdj_data['K'][date[i]]<kdj_data['D'][date[i]]:
                    state = 'BOTTOM'
                    sell_price = price[i]
                    income = (sell_price - buy_price)/buy_price * 100
                    income_total = income_total + income
                    sell_date = date[i]
                    update_result = [(buy_date, sell_date, buy_price, sell_price, income, income_total)]

                    print(stock_code,update_result)
                    self.load.write(stock_code, update_result)
                    cnt = cnt + 1
                    
        self.load.write_all_stock([(stock_code, income_total/cnt)])
        print('stock_code',[(stock_code, income_total/cnt)])
