# coding: utf8

import os

import easyutils
import pandas as pd
import numpy as np
import tushare as ts


def use(export='csv', **kwargs):
    if export.lower() in ['csv']:
        return CSVLoadStore(**kwargs)


class LoadStore:
    def read(self, stock_code):
        pass

    def write(self, stock_code, data):
        pass


class CSVLoadStore(LoadStore):
    def __init__(self, path_data, path_result, dtype):
        if dtype.lower() in ['d']:
            self.path = os.path.join(path_data, 'day')
        #self.result_path = os.path.join(self.path, 'data')
        self.raw_path = self.path#os.path.join(self.path, 'raw_data')
        self.result_path = os.path.join(path_result, 'preprocess')
        
    def read(self, stock_code):
        if not os.path.exists(self.raw_path):
            print('this folder is not exist({}.%s)',self.raw_path)
            raise IOError
        csv_file_path = os.path.join(self.result_path, '{}_trade.csv'.format(stock_code))
        if os.path.exists(csv_file_path):
            try:
#['date', 'open', 'high', 'd', 'low', 'volume', 'amount', 'factor']
                his = pd.read_csv(csv_file_path)
            except ValueError:
                return
        return his
    def read_with_date(self, stock_code,date_start, date_end):
        if not os.path.exists(self.raw_path):
            print('this folder is not exist({}.%s)',self.raw_path)
            raise IOError
        csv_file_path = os.path.join(self.raw_path, '{}.csv'.format(stock_code))
        if os.path.exists(csv_file_path):
            try:
#['date', 'open', 'high', 'd', 'low', 'volume', 'amount', 'factor']
                his = pd.read_csv(csv_file_path)
            except ValueError:
                return
        selectend_his = his[his.date <= date_end]
        select_his = selectend_his[selectend_his.date >= date_start]
        #data_len = len(select_his)
        #index =np.linspace(0,data_len-1,data_len)
        #index.astype(np.uint32)
        #select_his = select_his.set_index(index)
        #and his.date <= date_end
        return select_his
      
    def load_processing_data_with_date(self, stock_code,date_start, date_end):
        if not os.path.exists(self.result_path):
            print('this folder is not exist({}.%s)',self.result_path)
            raise IOError
          
        csv_file_path = os.path.join(self.result_path, '{}_trade.csv'.format(stock_code))
        if not os.path.exists(csv_file_path):
            print('this folder is not exist({}.%s)',csv_file_path)
            raise IOError
        if os.path.exists(csv_file_path):
            try:
#['date', 'open', 'high', 'd', 'low', 'volume', 'amount', 'factor']
                his = pd.read_csv(csv_file_path)
            except ValueError:
                return
        selectend_his = his[his.date <= date_end]
        select_his = selectend_his[selectend_his.date >= date_start]
        #data_len = len(select_his)
        #index =np.linspace(0,data_len-1,data_len)
        #index.astype(np.uint32)
        #select_his = select_his.set_index(index)
        #and his.date <= date_end
        return select_his
    
    def write(self, stock_code, updated_data):
        if not os.path.exists(self.result_path):
            os.makedirs(self.result_path)
        csv_file_path = os.path.join(self.result_path, '{}_trade.csv'.format(stock_code))
        if os.path.exists(csv_file_path):
            try:
                his = pd.read_csv(csv_file_path)
            except ValueError:
                return

            update_data = pd.DataFrame(updated_data, columns=his.columns)
            old_date = his['date'].iloc[-1]
            his = his.append(update_data[update_data.date > old_date])
        else:
            his = pd.DataFrame(updated_data,columns=['date','open','close','high','low','volume'])
            #his = pd.DataFrame(columns=['date_buy', 'date_sell', 'price_buy', 'price_sell', 'income', 'income_total'])
        his.to_csv(csv_file_path, index=False)
    
    def write_all_stock(self, updated_data):
        if not os.path.exists(self.result_path):
            os.makedirs(self.result_path)
        csv_file_path = os.path.join(self.result_path, 'all_stock_final_trade.csv')
        if os.path.exists(csv_file_path):
            try:
                his = pd.read_csv(csv_file_path)
            except ValueError:
                return

            #old_his = updated_data[0][0]
            #old_his = his[his.date_buy < updated_data_start_date]
            updated_his = pd.DataFrame(updated_data, columns=his.columns)
            his = his.append(updated_his)
        else:
            his = pd.DataFrame(updated_data,columns=['stock_code', 'income_total'])
            #his = pd.DataFrame(columns=['date_buy', 'date_sell', 'price_buy', 'price_sell', 'income', 'income_total'])
        his.to_csv(csv_file_path, index=False)
    
    def get_trade_date(self,start_date,end_date):
        sh_data = ts.get_k_data('sh',start=start_date,end=end_date)
        trade_date = sh_data['date']
        return trade_date
                
    @property
    def init_stock_codes(self):
        stock_codes = easyutils.stock.get_all_stock_codes()
        exists_codes = set()
        if os.path.exists(self.raw_path):
            code_slice = slice(-4)
            exists_codes = {code[code_slice] for code in os.listdir(self.raw_path) if code.endswith('.csv')}
        return set(stock_codes).difference(exists_codes)

    @property
    def update_stock_codes(self):
        code_slice = slice(6)
        stock = [f[code_slice] for f in os.listdir(self.raw_path) if f.endswith('.json')]
        stock = sorted(stock)
        return stock
    
if __name__ == '__main__':
    Load = use(export='csv',path_data='../easyhistory/history/',path_result='/income/',dtype='D')
    stock_codes = Load.update_stock_codes
    data = Load.read('000001')
