# -*- coding: utf-8 -*-

from .analysisvolumeprice import Analysisvolumeprice
from .analysisVPwithdate import analysisVPwithdate
from .ta_back_test import ta_back_test_withdate

def analysis(path='../../easyhistory/history/', path_income='../income/', suite='STRATEGYBOTTOMTOP'):
    #return Analysisvolumeprice(path=path, path_income=path_income, suite=suite).processing('300183')
    return Analysisvolumeprice(path=path, path_income=path_income, suite=suite).volume_price_thread()

def analysiswithdate(path='../../easyhistory/history/', path_income='../incomewithdate/', suite='STRATEGYBOTTOMTOP'):
    #return Analysisvolumeprice(path=path, path_income=path_income, suite=suite).processing('300183')
    return analysisVPwithdate(path=path, path_income=path_income, suite=suite).volume_price_thread()
  
def trade_ta_back_test(path='../../easyhistory/history/', path_income='../incomewithdate/', suite='defaults'):
    #return Analysisvolumeprice(path=path, path_income=path_income, suite=suite).processing('300183')
    return ta_back_test_withdate(path=path, path_income=path_income, suite=suite).trade_back_test_thread()