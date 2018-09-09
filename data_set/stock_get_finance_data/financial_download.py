#-*- coding:UTF-8 -*-
from urllib import request
import os
import tushare as ts
import pandas as pd

MAIN_FINANCE = 'http://quotes.money.163.com/service/zycwzb_{}.html?type=report'
ADBSTRACT_FINANCE = 'http://quotes.money.163.com/service/cwbbzy_{}.html'
PROFIT_FINANCE = 'http://quotes.money.163.com/service/lrb_{}.html'
CASH_FINANCE = 'http://quotes.money.163.com/service/xjllb_{}.html'
LOANS_FINANCE = 'http://quotes.money.163.com/service/zcfzb_{}.html'

def Schedule(a,b,c):
    per = 100.0 * a * b / c
    if per > 100 :
        per = 100
    print('%.2f%%' % per)
    
def try_download_csv(url,local,Schedule,stock):
  try:
    request.urlretrieve(url,local,Schedule)
    continue_download_this_stock = 0
  except :
    print('fail to download stock ',stock, 'one times, and try it again!!!');
    continue_download_this_stock = 1
  return continue_download_this_stock

def fetch_stock_finance_data(path,stock):
  #main finance
  url = MAIN_FINANCE.format(stock)
  local = os.path.join(path,'{}_main.csv'.format(stock))
  continue_download_this_stock = try_download_csv(url,local,Schedule,stock)
  if continue_download_this_stock==1:
    return continue_download_this_stock
  
  #abstract
  url = ADBSTRACT_FINANCE.format(stock)
  local = os.path.join(path,'{}_abstract.csv'.format(stock))
  continue_download_this_stock = try_download_csv(url,local,Schedule,stock)
  if continue_download_this_stock==1:
    return continue_download_this_stock
  #profit
  url = PROFIT_FINANCE.format(stock)
  local = os.path.join(path,'{}_profit.csv'.format(stock))
  continue_download_this_stock = try_download_csv(url,local,Schedule,stock)
  if continue_download_this_stock==1:
    return continue_download_this_stock
  #cash
  url = CASH_FINANCE.format(stock)
  local = os.path.join(path,'{}_cash.csv'.format(stock))
  continue_download_this_stock = try_download_csv(url,local,Schedule,stock)
  if continue_download_this_stock==1:
    return continue_download_this_stock
  #loans
  url = LOANS_FINANCE.format(stock)
  local = os.path.join(path,'{}_loans.csv'.format(stock))
  continue_download_this_stock = try_download_csv(url,local,Schedule,stock)
  if continue_download_this_stock==1:
    return continue_download_this_stock

def ts_stock_codes():
  basic_data = ts.get_stock_basics()
  stockcode = list(basic_data.index)
  stockcode.sort()
  return stockcode

def read_stock_index(download_stock_file):
  stocks_index = 0
  if os.path.exists(download_stock_file):
    try:
        his = pd.read_csv(download_stock_file)
        stocks_index = int(his.columns[1])
    except ValueError:
        return
  return stocks_index

def store_stock_index(download_stock_file, stock_index):
  his = pd.Series(stock_index)
  his.to_csv(download_stock_file)

if __name__ == '__main__':
  
  stock_codes=ts_stock_codes()
  
  path_root = '../../../data/'
  
  path = os.path.join(path_root,'finance')
  if not os.path.exists(path):
            os.makedirs(path)
            
  download_stock_file = os.path.join(path_root,'stock_index.csv')
  stock_index = read_stock_index(download_stock_file)
  stock_codes = stock_codes[stock_index:]
  
  for stock in (stock_codes):
    print("fetching stock",stock)
    continue_download_this_stock = 1
    while continue_download_this_stock == 1:
        continue_download_this_stock = fetch_stock_finance_data(path,stock)
    store_stock_index(download_stock_file, stock_index)
    stock_index = stock_index + 1
    print("fetched stock",stock)
  


