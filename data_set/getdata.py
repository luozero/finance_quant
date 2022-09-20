import trady_data
import stock_process_day_data
import tushare as ts
from _tracemalloc import start

#trady_data.init(dtype='D', export='csv', path='./data/stocktradedata/')


#trady_data.update_single_code(dtype='D', stock_code='000002', path='./data/stocktradedata/', export='csv')
#trady_data.update(path='./data/stocktradedata/', export='csv')

start_date = '2014-01-09'
end_date = '2018-07-29'

path='../../data/download/'
stockcode = ['000001','000002','000018','600000','600005','600007']
basic_data = ts.get_stock_basics()
stockcode = list(basic_data.index)
stockcode.remove('603657')
stockcode.sort()


trady_data.updateWithDate(path=path, export='csv',\
                                  dateStart=start_date,dateEnd=end_date,stock_codes=stockcode)

print("finished to get and process data")
