# -*- coding: utf-8 -*-

from .analysisvolumeprice import Analysisvolumeprice
from .analysisVPwithdate import analysisVPwithdate

def analysis(path='../../easyhistory/history/', path_income='../income/', suite='STRATEGYBOTTOMTOP'):
    #return Analysisvolumeprice(path=path, path_income=path_income, suite=suite).processing('300183')
    return Analysisvolumeprice(path=path, path_income=path_income, suite=suite).volume_price_thread()

def analysiswithdate(path='../../easyhistory/history/', path_income='../incomewithdate/', suite='STRATEGYBOTTOMTOP'):
    #return Analysisvolumeprice(path=path, path_income=path_income, suite=suite).processing('300183')
    return analysisVPwithdate(path=path, path_income=path_income, suite=suite).volume_price_thread()