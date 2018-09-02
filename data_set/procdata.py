import stock_get_day_data
import stock_process_day_data
import tushare as ts
from _tracemalloc import start

#stock_get_day_data.init(dtype='D', export='csv', path='./data/stocktradedata/')


#stock_get_day_data.update_single_code(dtype='D', stock_code='000002', path='./data/stocktradedata/', export='csv')
#stock_get_day_data.update(path='./data/stocktradedata/', export='csv')

start_date = '2014-01-09'
end_date = '2018-07-29'

path='../../data/stocktradedata/'
path_result='../../data/pctdata'
#stockcode = ['000001','000002','000018','600000','600005','600007']
basic_data = ts.get_stock_basics()
stockcode = list(basic_data.index)
stockcode.remove('603657')
stockcode.remove('300724')
stockcode.remove('603192')
stockcode.remove('601068')
stockcode.sort()
stockcode = stockcode[3342:-1]


stock_process_day_data.stock_trade_preprocess(export='csv',path_data=path, \
                                              path_result=path_result,dtype='D',\
                           start_date=start_date,end_date=end_date, stocks=stockcode)
print("finished to get and process data")
