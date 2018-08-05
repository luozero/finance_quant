# coding: utf-8
import math
import re
import time
import sys
import tushare as ts
from datetime import datetime
from datetime import timedelta
from multiprocessing.pool import ThreadPool

import requests
from pyquery import PyQuery

from . import helpers
from . import store


class Day:
    SINA_API = 'http://vip.stock.finance.sina.com.cn/corp/go.php/vMS_FuQuanMarketHistory/stockid/{stock_code}.phtml'
    SINA_API_HOSTNAME = 'vip.stock.finance.sina.com.cn'
    STOCK_CODE_API = 'http://218.244.146.57/static/all.csv'

    def __init__(self, path='history', export='csv'):
        self.store = store.use(export=export, path=path, dtype='D')
#################################################################################
    def init(self):
        stock_codes = self.store.init_stock_codes
        pool = ThreadPool(10)
        pool.map(self.init_stock_history, stock_codes)

    def init_stock_history(self, stock_code):
        #all_history = self.get_all_history(stock_code)
        print("geting all stock", stock_code)
        all_history = ts.get_k_data(stock_code)
        if all_history is None:
            return
        #all_history = all_history.reset_index()
        self.store.write(stock_code, all_history)
#################################################################################
    def update(self):
        """ 更新已经下载的历史数据 """
        stock_codes = self.store.update_stock_codes
        pool = ThreadPool(2)
        pool.map(self.update_single_code, stock_codes)

    def update_single_code(self, stock_code):
        """ 更新对应的股票文件历史行情
        :param stock_code: 股票代码
        :return:
        """
        print("geting single stock", stock_code)
        latest_date = self.store.get_his_stock_date(stock_code)
        updated_data = self.get_update_day_history(stock_code, latest_date)
        
        if len(updated_data) == 0 or len(updated_data[0]) == 0:
          print("output data is null, the stock is ", stock_code)
          sys.exit()

        self.store.write(stock_code, updated_data)

    def get_update_day_history(self, stock_code, latest_date):
        latest_nextday = latest_date + timedelta(days=1)
        now = datetime.now()
        
        date_start_str = latest_nextday.strftime("%Y-%m-%d");
        date_end_str = now.strftime("%Y-%m-%d");
        updated_data = ts.get_k_data(stock_code,start=date_start_str,end=date_end_str)
        
        if date_start_str>date_end_str:
            print("update date err", "start date", date_start_str,"end date", date_end_str)
            return
        
        if updated_data is None:
          print("output data is null, the stock is ", stock_code)
          sys.exit()
        #updated_data = updated_data.reset_index()
        return updated_data
#################################################################################
    def updatewithDate(self, dateStart,dateEnd,stock_codes):
        self.dateStart=dateStart
        self.dateEnd=dateEnd
        #stock_codes = self.store.update_stock_codes
        pool = ThreadPool(2)
        pool.map(self.update_single_code_withDate, stock_codes)
        
    def update_single_code_withDate(self, stock_code):
        date_start_str = self.dateStart
        date_end_str = self.dateEnd
        updated_data = ts.get_k_data(stock_code,start=date_start_str,end=date_end_str)
        print("geting single stock", stock_code,"start date",date_start_str,"end date",date_end_str)
        
        if date_start_str>date_end_str:
            print("update date err", "start date", date_start_str,"end date", date_end_str)
            return
        
        if updated_data is None:
          print("output data is null, the stock is ", stock_code)
          sys.exit()
        #updated_data = updated_data.reset_index()
        
        if len(updated_data) == 0:# or len(updated_data[0]) == 0:
          print("output data is null, the stock is ", stock_code)
          sys.exit()

        self.store.write(stock_code, updated_data)        
