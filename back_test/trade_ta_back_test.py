# -*- coding: utf-8 -*-

import trade_back_test

path_in='../../data/download/'
path_out='../../data/vp/'

#easyvolumeprice.analysiswithdate(path='../easyhistory/history/', path_income='./incomewithdate/STRATEGYBOTTOMTOP2/', suite='STRATEGYBOTTOMTOP2')
#easyvolumeprice.analysis(path='../easyhistory/history/', path_income='./income/', suite='STRATEGYBOTTOMTOP1')
trade_back_test.trade_ta_back_test(path=path_in, path_income=path_out, suite='defaults')

