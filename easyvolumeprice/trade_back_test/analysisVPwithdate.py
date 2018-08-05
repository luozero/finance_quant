# -*- coding: utf-8 -*-

from . import load
from . import conf
from . import strategyVP

#import load
#import conf
#import strategyVP

import time

from multiprocessing.pool import ThreadPool

def use(**kwargs):
        return analysisVPwithdate(**kwargs)
    
class analysisVPwithdate:
    def __init__(self, path='../../easyhistory/history/', path_income='../income/', suite='defaults'):
        self.load = load.use(export='csv', path=path, path_income=path_income, dtype='D')
        confpara = conf.load_conf('stockdate.conf')
        config = dict(confpara[suite])
        self.volume_bottom_coeff = float(config['volumebottomcoeff'])
        self.price_bottom_coeff = float(config['pricebottomcoeff'])
        #self.duration_bottom = int(config['durationbottom'])
        self.volume_top_coeff = float(config['volumetopcoeff'])
        self.price_top_coeff = float(config['pricetopcoeff'])
        self.duration_top = int(config['durationtop'])
        self.daily_limit_rate = float(config['dailylimitrate'])
        self.date_start= config['datestart']
        self.date_end= config['dateend']
        self.bottom_days = int(config['bottomdays'])
        self.bottom_days_thres = int(config['bottomdaysthres'])
        self.edge_days_thres = int(config['edgedaysthres'])
        self.edge_days = int(config['edgedays'])
        self.edge_coeffvol = float(config['edgecoeffvol'])
        self.edge_coeffpri = float(config['edgecoeffpri'])
        self.stock_codes = config['stock_codes'].split(',')
        #load strategy
        self.strategy = strategyVP.use(data=False)
        
    def volume_price_thread(self):
        #stock_codes = self.load.update_stock_codes
        stock_codes = self.stock_codes
       # date_start = self.date_start
       # date_end = self.date_end
        #stock_codes = {'159942','600000', '002379','600519'}
        pool = ThreadPool(1)
        pool.map(self.processing, stock_codes)
        #self.processing(stock_codes)
        
    def load_volume_price_date(self,stock_code,date_start,date_end):
        data = self.load.read_with_date(stock_code,date_start,date_end)
        data_factor = 1#data['factor'].max()
        data_price = data['close']
        data_volume = data['volume']/data_factor
        data_price = data_price/data_factor
        data_date = data['date']
        return (data_volume,data_price,data_date)
        
    def processing(self, stock_code):
 
        date_start = self.date_start
        date_end = self.date_end
        #print('load start----------------',stock_code)
        volume, price, date = self.load_volume_price_date(stock_code,date_start,date_end)
        income_total = 0
        start_time = self.bottom_days + self.edge_days +1
        length = len(volume)
        
        state = 'BOTTOM'
        cnt = 0.000001
        for i in range(start_time,length):
            if state == 'BOTTOM':
                buy_rate_flag = self.strategy.process_daily_limit(price, i, self.daily_limit_rate)
                #print(date[i])
                #buyflag = self.strategy.processingVP(i,volume,price, self.duration_bottom, self.volume_bottom_coeff, self.price_bottom_coeff,
                 #                                  self.bottom_days, 'POS')
                #buyflag = self.strategy.processingVP_withDurationBottom(i,volume,price, self.duration_bottom, self.volume_bottom_coeff, self.price_bottom_coeff,
                #                                   self.bottom_days, self.bottom_days_thres, self.edge_days, self.edge_days_thres,self.edge_coeffvol,self.edge_coeffpri)
                #buyflag = self.strategy.processingVP_withDurationBottomFixMeanVar(i,volume,price, self.duration_bottom, self.volume_bottom_coeff, self.price_bottom_coeff,
                #                                   self.bottom_days, self.bottom_days_thres, self.edge_days, self.edge_days_thres,self.edge_coeffvol,self.edge_coeffpri)
                buyflag = self.strategy.processingVP_range_strategy(date[i], i,volume,price, self.volume_bottom_coeff, self.price_bottom_coeff,
                                                   self.bottom_days, self.bottom_days_thres, self.edge_days, self.edge_days_thres,self.edge_coeffvol,self.edge_coeffpri, 'POS')

                if buyflag and buy_rate_flag:
                    state = 'HOLD'
                    buy_price = price[i]
                    buy_date = date[i]
            elif state == 'HOLD':
                #sell_volume_flag = self.strategy.processing_edge(volume, i, self.duration_top, self.volume_top_coeff, 'NEG')
                #sell_price_flag = self.strategy.processing_edge(price, i, self.duration_top, self.price_top_coeff, 'NEG')
                sellflag = self.strategy.processingVP_top_strategy(i,volume,price, self.duration_top, self.volume_top_coeff, self.price_top_coeff,'NEG')
                if sellflag:
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

if __name__ == '__main__':
    analysis_volume_price = use(path='../../easyhistory/history/', path_income='../incomewithdate/', suite='STRATEGYBOTTOMTOPWITHDATA')
    #a = Analysisvolumeprice(path='../easyhistory/history/', path_income='/income/', suite='defaults')
    analysis_volume_price.processing('000739')
    #analysis_volume_price.volume_price_thread()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        


