# coding: utf8
import pandas as pd
import numpy as np
import os
import tushare as ts
import financial_download
from financial_load_store import financial_load_store as FLS

finance_index_dic = {
  #####earning capacity
  'roe':'roe','roa':'roa','profit_revenue':'profit_revenue','profit_cost':'profit_cost','equlity_incr_rate':'equlity_incr_rate',
  ###grow capacity
  'revenue_incr_rate':'revenue_incr_rate','profit_incr_rate':'profit_incr_rate',
  'cash_incr_rate':'cash_incr_rate','asset_incr_rate':'asset_incr_rate','debt_incr_rate':'debt_incr_rate',
  ###asset struct
  'debt_asset_ratio':'debt_asset_ratio','debt_equality_ratio':'debt_equality_ratio','debt_net_asset_ratio':'debt_net_asset_ratio',
  'revenue_asset_ratio':'revenue_asset_ratio','goodwell_equality_ratio':'goodwell_equality_ratio','dev_rev_ratio':'dev_rev_ratio',
  ##enterprise value
  'CFO2EV':'CFO2EV','EDITDA2EV':'EDITDA2EV',
  'E2PFY0':'E2PFY0','E2PFY1':'E2PFY1',
  'BB2P':'BB2P','BB2EV':'BB2EV',
  'B2P':'B2P','S2EV':'S2EV',
  ##quality
  'RNOA':'RNOA','CFROI':'CFROI','OL':'OL','OLinc':'OLinc','WCinc':'WCinc','NCOinc':'NCOinc',
  'icapx':'icapx','capxG':'capxG','XF':'XF','shareInc':'shareInc',
  }
class financail_factor_calc:
  def __init__(self, path='../../../data/'):
    self.path = path
    self.FLS = FLS(path)
  def ab_ratio_calc(self, a,b,str):
    data = a/b
    data[np.isinf(data)]=0
    data[np.isnan(data)]=0
    data = data.dot(100)
    dict_data = {str:data}
    pd_data = pd.DataFrame(dict_data)
    return pd_data
  def qoq_rate_calc(self, a,str):
    data = (a[:-4]-a[4:])/a[4:]
    data = data.dot(100)
    data[np.isinf(data)]=0
    data = np.append(data,[0,0,0,0])
    dict_data = {str:data}
    pd_data = pd.DataFrame(dict_data)
    return pd_data
  def abc_ratio_calc(self, a,b,c,str,op):
    if(op=='sub'):
      data = a/(b-c)
    data[np.isinf(data)]=0
    dict_data = {str:data}
    pd_data = pd.DataFrame(dict_data)
    return pd_data
  
  def financial_index_calc(self,stock_code):
    equlity = self.FLS.fetch_one_financial_factor_in_stock('main','股东权益不含少数股东权益(万元)')
    asset = self.FLS.fetch_one_financial_factor_in_stock('main','总资产(万元)')
    revenue = self.FLS.fetch_one_financial_factor_in_stock('main','主营业务收入(万元)')
    cash = self.FLS.fetch_one_financial_factor_in_stock('main','经营活动产生的现金流量净额(万元)')
    debt = self.FLS.fetch_one_financial_factor_in_stock('main','总负债(万元)')
    
    earning = self.FLS.fetch_one_financial_factor_in_stock('profit','净利润(万元)')
    cost = self.FLS.fetch_one_financial_factor_in_stock('profit','营业总成本(万元)')
   
    equality = self.FLS.fetch_one_financial_factor_in_stock('loans','所有者权益(或股东权益)合计(万元)')
    intangible_asset = self.FLS.fetch_one_financial_factor_in_stock('loans','无形资产(万元)')
    dev_cost = self.FLS.fetch_one_financial_factor_in_stock('loans','开发支出(万元)')
    goodwell = self.FLS.fetch_one_financial_factor_in_stock('loans','商誉(万元)')
   
    EV = self.FLS.fecth_one_stock_basic_in_stock(stock_code,'total_mv')
    #####earning capacity
    #roe
    roe = self.ab_ratio_calc(earning,equlity,'roe')
    pd_data = roe
    #roa
    roa = self.ab_ratio_calc(earning,asset,'roa')
    pd_data = pd.concat([pd_data, roa], axis=1)
    #profit_revenue
    profit_revenue = self.ab_ratio_calc(earning,revenue,finance_index_dic['profit_revenue'])
    pd_data = pd.concat([pd_data, profit_revenue], axis=1)
    #profit_cost
    profit_cost = self.ab_ratio_calc(earning,cost,finance_index_dic['profit_cost'])
    pd_data = pd.concat([pd_data, profit_cost], axis=1)
    #stackholder equality increase
    equlity_incr_rate = self.qoq_rate_calc(equality,finance_index_dic['equlity_incr_rate'])
    pd_data = pd.concat([pd_data, equlity_incr_rate], axis=1)
  
    ###grow capacity
    #revenue
    revenue_incr_rate = self.qoq_rate_calc(revenue,finance_index_dic['revenue_incr_rate'])
    pd_data = pd.concat([pd_data, revenue_incr_rate], axis=1)
    #profit
    profit_incr_rate = self.qoq_rate_calc(earning,finance_index_dic['profit_incr_rate'])
    pd_data = pd.concat([pd_data, profit_incr_rate], axis=1)
    #cash
    cash_incr_rate = self.qoq_rate_calc(cash,finance_index_dic['cash_incr_rate'])
    pd_data = pd.concat([pd_data, cash_incr_rate], axis=1)
    #asset
    asset_incr_rate = self.qoq_rate_calc(asset,finance_index_dic['asset_incr_rate'])
    pd_data = pd.concat([pd_data, asset_incr_rate], axis=1)
    #debt
    debt_incr_rate = self.qoq_rate_calc(debt,finance_index_dic['debt_incr_rate'])
    pd_data = pd.concat([pd_data, debt_incr_rate], axis=1)
    
    ###asset struct
    #debt_asset_ratio
    debt_asset_ratio = self.ab_ratio_calc(debt,asset,finance_index_dic['debt_asset_ratio'])
    debt_asset_ratio = debt_asset_ratio/100
    pd_data = pd.concat([pd_data, debt_asset_ratio], axis=1)
    #debt_equality_ratio
    debt_equality_ratio = self.ab_ratio_calc(debt,equality,finance_index_dic['debt_equality_ratio'])
    debt_equality_ratio = debt_equality_ratio/100
    pd_data = pd.concat([pd_data, debt_equality_ratio], axis=1)
    #debt_net_asset_ratio
    debt_net_asset_ratio = self.abc_ratio_calc(debt,equality,intangible_asset,finance_index_dic['debt_net_asset_ratio'],'sub')
    pd_data = pd.concat([pd_data, debt_net_asset_ratio], axis=1)
    #revenue_asset_ratio
    revenue_asset_ratio = self.ab_ratio_calc(revenue,asset,finance_index_dic['revenue_asset_ratio'])
    revenue_asset_ratio = revenue_asset_ratio
    pd_data = pd.concat([pd_data, revenue_asset_ratio], axis=1)
    #goodwell_equality_ratio
    goodwell_equality_ratio = self.ab_ratio_calc(goodwell,equality,finance_index_dic['goodwell_equality_ratio'])
    pd_data = pd.concat([pd_data, goodwell_equality_ratio], axis=1)
    
    ###CFO2EV
    dev_rev_ratio = self.ab_ratio_calc(cash,EV,finance_index_dic['CFO2EV'])
    pd_data = pd.concat([pd_data, dev_rev_ratio], axis=1)
    
    pd_data.index = self.FLS.all_financial_one_stock['main'].iloc[0,:].index[1:]
    return pd_data #pd.DataFrame([roe roa profit_revenue profit_cost])
  
def main_financial_data_process(path):
  stock_codes = financial_download.ts_stock_codes()
  FFC =financail_factor_calc(path=path)
  stock_codes = ['000001']
  for stock_code in stock_codes:
    print("stock:",stock_code)
    FFC.FLS.load_all_financial_one_stock(stock_code)
    FFC.FLS.load_all_stock_basic_one_stock([stock_code])
    data_processed = FFC.financial_index_calc(stock_code)
    FFC.FLS.store_process_financical_data(data_processed, stock_code)
    
if __name__ == '__main__':
  #stock_codes = ['000001','000002','000004']
  
  path = '../../../data/'
  main_financial_data_process(path)
  print("processed successfully!!!")
 # data_main = data[0]

