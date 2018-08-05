# -*- coding: utf-8 -*-

import easyvolumeprice

path_in='../stock_data/stockdata/download/'
path_out='../stock_data/stockdata/vp/'

#easyvolumeprice.analysiswithdate(path='../easyhistory/history/', path_income='./incomewithdate/STRATEGYBOTTOMTOP2/', suite='STRATEGYBOTTOMTOP2')
#easyvolumeprice.analysis(path='../easyhistory/history/', path_income='./income/', suite='STRATEGYBOTTOMTOP1')
easyvolumeprice.analysiswithdate(path=path_in, path_income=path_out, suite='STRATEGY1')

