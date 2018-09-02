# coding: utf8

'''
Created on 2018��4��7��

@author: ll
'''
import pandas as pd
import numpy as np
import time, datetime
import stock_get_day_data
from datetime import timedelta
from datetime import datetime
from . import loadstore
#import loadstore
#from conda.plan import _update_old_plan

#from portfoliostock.stockportfolio.loadstore import stock_codes
#from odo.backends.tests.test_sas import columns

class process_day_data(object):
    '''
    classdocs
    '''
    def __init__(self, load_data,start_date, end_date):
        '''
        Constructor
        '''
        self.load_data = load_data
        self.start_date = start_date
        self.end_date = end_date
        self.trade_date = load_data.get_trade_date(start_date,end_date)
    
    def load_stock_data_and_align_processing(self,stock):
        trade_date = self.load_data.get_trade_date(self.start_date,self.end_date);
        stock_data = self.load_data.read_with_date(stock,self.start_date,self.end_date)
        stock_df = pd.DataFrame(np.zeros([len(trade_date),6]),columns=['date','open','close','high','low','volume'])
        trade_date = trade_date.reset_index()
        stock_df.date = trade_date.date
        
        stock_data_date = stock_data.date
        stock_data = stock_data.set_index('date')
        stock_df_date = stock_df.date
        stock_df = stock_df.set_index('date')
        
        date_old1 = datetime.strptime(stock_df_date[0], "%Y-%m-%d")
        date_old1 = date_old1-timedelta(days=1)
        date_old = date_old1.strftime("%Y-%m-%d")
        
        for date in stock_data_date:
            date_range = stock_df_date[stock_df_date<=date]
            date_range =  date_range[stock_df_date>date_old]
            for date_sub in date_range:
                stock_df.loc[date_sub]= stock_data.loc[date]
            date_old = date

        return stock_df
    
    def calc_stock_price_rate(self,stock_data):
        #price = stock_data.close
        rate = (stock_data[:len(stock_data)-1] - stock_data[1:]) / stock_data[1:]
        return pd.DataFrame(rate)

    def preprocessing_api(self,stock_codes):
        iteration = 0
        price_rate = pd.DataFrame(index=self.trade_date)
        for stock in stock_codes:
            print('iteration is',iteration,'processing stock is',stock)
            iteration = iteration + 1
            stock_data_align = self.load_stock_data_and_align_processing(stock)
            stock_price_rate = stock_data_align.pct_change(periods=1)
            #stock_price_rate['date'] = stock_price_rate.index
            stock_price_rate = stock_price_rate.reset_index()
            self.load_data.write(stock,stock_price_rate)

if __name__ == '__main__':
    #stock_get_day_data.update_single_code(dtype='D', '000001', path_data='../stockdata/stocktradedata', export='csv')
    load_data1 = loadstore.use(export='csv',path_data='../stockdata/stocktradedata', path_result='../stockdata/pctdata',dtype='D')
    process_day_data(load_data=load_data1,start_date='2014-01-01',end_date='2014-03-16').preprocessing_api(['000002'])
    
