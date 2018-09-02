# coding:utf-8
from .process_day_data import process_day_data
from . import loadstore

def stock_trade_preprocess(export='csv',path_data='../stockdata/stocktradedata', path_result='../stockdata/pctdata',dtype='D',\
                           start_date='2014-01-01',end_date='2014-03-16', stocks=['000002']):
    load_data1 = loadstore.use(export=export, path_data=path_data, path_result=path_result, dtype=dtype)
    process_day_data(load_data=load_data1,start_date=start_date,end_date=end_date).preprocessing_api(stocks)