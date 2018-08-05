# -*- coding: utf-8 -*-

from . import load
from . import conf

import numpy as np

#import load
#import conf

from multiprocessing.pool import ThreadPool

def use(**kwargs):
        return Analysisvolumeprice(**kwargs)
    
class Analysisvolumeprice:
    def __init__(self, path='../../easyhistory/history/', path_income='../income/', suite='defaults'):
        self.load = load.use(export='csv', path=path, path_income=path_income, dtype='D')
        confpara = conf.load_conf('stock.conf')
        config = dict(confpara[suite])
        self.volume_bottom_coeff = float(config['volumebottomcoeff'])
        self.price_bottom_coeff = float(config['pricebottomcoeff'])
        self.duration_bottom = int(config['durationbottom'])
        self.volume_top_coeff = float(config['volumetopcoeff'])
        self.price_top_coeff = float(config['pricetopcoeff'])
        self.duration_top = int(config['durationtop'])
        self.daily_limit_rate = float(config['dailylimitrate'])
        
    def volume_price_thread(self):
        stock_codes = self.load.update_stock_codes
        #stock_codes = {'159942','600000', '002379','600519'}
        pool = ThreadPool(10)
        pool.map(self.processing, stock_codes)
        #self.processing(stock_codes)
        
    def load_volume_price_date(self,stock_code):
        data = self.load.read(stock_code)
        data_factor = data['factor'].max()
        data_price = data['close']
        data_volume = data['volume']/data_factor
        data_price = data_price/data_factor
        data_date = data['date']
        return (data_volume,data_price,data_date)
        
    def processing_edge(self, data, start_time, duration, coeff, pos_neg):
        if start_time<=duration:
            print('start_time=%d is smaller than duration=%d',start_time,duration) 
            exit()
        flag = False

        data_mean = np.mean(data.iloc[start_time-duration-1:start_time-1])
        data_var = np.std(data.iloc[start_time-duration-1:start_time-1])

        if pos_neg == 'POS':
            if data.iloc[start_time]>data_mean+data_var*coeff:
                flag = True
        elif pos_neg == 'NEG':
            if data.iloc[start_time]<data_mean-data_var*coeff:
                flag = True
        return flag
    
    def process_daily_limit(self, data, start_time):
        price_today = data.iloc[start_time]
        price_yestoday = data.iloc[start_time-1]
        rate = (price_today - price_yestoday)*100/price_yestoday
        rate_flag = False
        if rate <= self.daily_limit_rate and rate>0:
            rate_flag = True
        #rate_flag = rate <= self.daily_limit_rate
        return rate_flag
        
    def processing(self, stock_code):
        #print('load start----------------',stock_code)
        volume, price, date = self.load_volume_price_date(stock_code)
        #print('load end----------------',stock_code)
        income_total = 0
        start_time = self.duration_bottom + 1
        length = len(volume)
        state = 'BOTTOM'
        cnt = 0.000001
        for i in range(start_time,length):
            if state == 'BOTTOM':
                buy_volume_flag = self.processing_edge(volume, i, self.duration_bottom, self.volume_bottom_coeff, 'POS')
                buy_price_flag = self.processing_edge(price, i, self.duration_bottom, self.price_bottom_coeff, 'POS')
                buy_rate_flag = self.process_daily_limit(price, i)
                if buy_volume_flag and buy_price_flag and buy_rate_flag:
                    state = 'HOLD'
                    buy_price = price[i]
                    buy_date = date[i]
            elif state == 'HOLD':
                sell_volume_flag = self.processing_edge(volume, i, self.duration_top, self.volume_top_coeff, 'NEG')
                sell_price_flag = self.processing_edge(price, i, self.duration_top, self.price_top_coeff, 'NEG')
                if sell_volume_flag and sell_price_flag:
                    state = 'BOTTOM'
                    sell_price = price[i]
                    income = (sell_price - buy_price)/buy_price * 100
                    income_total = income_total + income
                    sell_date = date[i]
                    update_result = [(buy_date, sell_date, buy_price, sell_price, income, income_total)]
                    self.load.write(stock_code, update_result)
                    cnt = cnt + 1
                    print(stock_code,update_result)
        self.load.write_all_stock([(stock_code, income_total/cnt)])

if __name__ == '__main__':
    analysis_volume_price = use(path='../../easyhistory/history/', path_income='../income/', suite='STRATEGYBOTTOMTOP')
    #a = Analysisvolumeprice(path='../easyhistory/history/', path_income='/income/', suite='defaults')
    analysis_volume_price.processing('603929')
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        


