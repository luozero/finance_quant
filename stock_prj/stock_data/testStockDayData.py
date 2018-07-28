import stock_get_day_data
import stock_process_day_data

#stock_get_day_data.init(dtype='D', export='csv', path='./stockdata/stocktradedata/')


#stock_get_day_data.update_single_code(dtype='D', stock_code='000002', path='./stockdata/stocktradedata/', export='csv')
#stock_get_day_data.update(path='./stockdata/stocktradedata/', export='csv')


stockcode = ['000001','000002','000018','600000','600005','600007']
#stockcode = ['000001']
stock_get_day_data.updateWithDate(path='./stockdata/stocktradedata/', export='csv',dateStart='2014-01-09',dateEnd='2018-04-07',stock_codes=stockcode)
stock_process_day_data.stock_trade_preprocess(export='csv',path_data='./stockdata/stocktradedata', path_result='./stockdata/pctdata',dtype='D',\
                           start_date='2014-01-01',end_date='2018-04-04', stocks=stockcode)
print("finished to get and process data");