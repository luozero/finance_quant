# coding: utf8
import pandas as pd
import os
import tushare as ts
import sys
sys.path.append('../stock_get_finance_data')
from financial_load_store import financial_load_store as FLS
from stock_deeplearning.ultility.stock_codes_utility import stock_codes_utility as SCU

finance_index_dic = {
  #####earning capacity
  'roe':'roe','roa':'roa','roi':'roi','profit_revenue':'profit_revenue','profit_cost':'profit_cost','equlity_incr_rate':'equlity_incr_rate',
  ###grow capacity
  'revenue_incr_rate':'revenue_incr_rate','profit_incr_rate':'profit_incr_rate',
  'cash_incr_rate':'cash_incr_rate','asset_incr_rate':'asset_incr_rate','debt_incr_rate':'debt_incr_rate',
  ###asset struct
  'debt_asset_ratio':'debt_asset_ratio','debt_equity_ratio':'debt_equity_ratio','debt_net_asset_ratio':'debt_net_asset_ratio',
  'revenue_asset_ratio':'revenue_asset_ratio','goodwell_equity_ratio':'goodwell_equity_ratio','dev_rev_ratio':'dev_rev_ratio',
  ##enterprise value
  'CFO2EV':'CFO2EV','EDITDA2EV':'EDITDA2EV',
  'E2PFY0':'E2PFY0','E2PFY1':'E2PFY1',
  'BB2P':'BB2P','BB2EV':'BB2EV',
  'B2P':'B2P','S2EV':'S2EV',
  'NCO2A':'NCO2A',
  'E2EV':'E2EV',
  ##quality
  'OL':'OL','OLinc':'OLinc','WCinc':'WCinc','NCOinc':'NCOinc',
  'icapx':'icapx','capxG':'capxG','XF':'XF','shareInc':'shareInc',
  }
class financail_factor_statistic:
  def __init__(self, path='../../../data/'):
    self.path = path
    if not os.path.exists(path):
      os.makedirs(path)
    self.FLS = FLS(path)

  def financial_index_calc(self,stock_code):
    equlity = self.FLS.fetch_one_financial_factor_in_stock('main','股东权益不含少数股东权益(万元)')
    asset = self.FLS.fetch_one_financial_factor_in_stock('main','总资产(万元)')
    revenue = self.FLS.fetch_one_financial_factor_in_stock('main','主营业务收入(万元)')
    cash = self.FLS.fetch_one_financial_factor_in_stock('main','经营活动产生的现金流量净额(万元)')
    debt = self.FLS.fetch_one_financial_factor_in_stock('main','总负债(万元)')
    
    earning = self.FLS.fetch_one_financial_factor_in_stock('profit','净利润(万元)')
    interest = self.FLS.fetch_one_financial_factor_in_stock('profit','利息支出(万元)')
    tax0 = self.FLS.fetch_one_financial_factor_in_stock('profit','所得税费用(万元)')
    #tax1 = self.FLS.fetch_one_financial_factor_in_stock('profit','营业税金及附加(万元)')
    cost = self.FLS.fetch_one_financial_factor_in_stock('profit','营业总成本(万元)')
    EBIT = earning + interest + tax0
   
    equity = self.FLS.fetch_one_financial_factor_in_stock('loans','所有者权益(或股东权益)合计(万元)')
    debt_total = self.FLS.fetch_one_financial_factor_in_stock('loans','负债合计(万元)')
    intangible_asset = self.FLS.fetch_one_financial_factor_in_stock('loans','无形资产(万元)')
    dev_cost = self.FLS.fetch_one_financial_factor_in_stock('loans','开发支出(万元)')
    goodwell = self.FLS.fetch_one_financial_factor_in_stock('loans','商誉(万元)')
    fix_asset = self.FLS.fetch_one_financial_factor_in_stock('loans','固定资产(万元)')
    noncurrent_asset = intangible_asset + goodwell + fix_asset
    
    
    depreciation = self.FLS.fetch_one_financial_factor_in_stock('cash',' 固定资产折旧、油气资产折耗、生产性物资折旧(万元)')
    amortize0 = self.FLS.fetch_one_financial_factor_in_stock('cash',' 无形资产摊销(万元)')
    amortize1 = self.FLS.fetch_one_financial_factor_in_stock('cash',' 长期待摊费用摊销(万元)')
    excess_cash = self.FLS.fetch_one_financial_factor_in_stock('cash',' 现金的期末余额(万元)')
    #cash_quivalent = self.FLS.fetch_one_financial_factor_in_stock('cash',' 期末现金及现金等价物余额(万元)')
    cash_quivalent = self.FLS.fetch_one_financial_factor_in_stock('cash',' 加:期初现金及现金等价物余额(万元)')
    
    divedends = self.FLS.fetch_one_financial_factor_in_stock('cash',' 分配股利、利润或偿付利息所支付的现金(万元)')
    EBITDA = EBIT + depreciation +amortize0 + amortize1
 
    market_cap = self.FLS.fecth_one_stock_basic_in_stock(stock_code,'total_mv')
    EV = market_cap + debt - excess_cash
    
    pd_data = pd.DataFrame({'equlity':equlity})
    pd_data = pd.concat([pd_data, pd.DataFrame({'asset':asset})], axis=1)
    pd_data = pd.concat([pd_data, pd.DataFrame({'revenue':revenue})], axis=1)
    pd_data = pd.concat([pd_data, pd.DataFrame({'cash':cash})], axis=1)
    pd_data = pd.concat([pd_data, pd.DataFrame({'debt':debt})], axis=1)
    pd_data = pd.concat([pd_data, pd.DataFrame({'earning':earning})], axis=1)
    pd_data = pd.concat([pd_data, pd.DataFrame({'market_cap':market_cap})], axis=1)
    
    pd_data.index = self.FLS.all_financial_one_stock['main'].iloc[0,:].index[1:]
    pd_data = pd_data.sort_index(ascending=True)
    return pd_data #pd.DataFrame([roe roa profit_revenue profit_cost])
  
def main_financial_statistic_process(path):
  store_path = os.path.join(path,'statistic/')
  if not os.path.exists(store_path):
      os.makedirs(store_path)
  scu = SCU(path=path)
  stock_codes = scu.stock_codes_remove_no_stock_basic()
  FFC =financail_factor_statistic(path=path)
  
  sz50 = ts.get_sz50s()
  stock_codes = sz50['code']
  
  stock_industry = ts.get_industry_classified()
  stock_codes = stock_industry[stock_industry['c_name'].isin(['房地产'])]['code']
  #stock_codes = stock_codes.pop('000527')
  
  #stock_codes = ['000001','000002','000004']
  statistic_stock_data = {}
  statistic_stock_min_len = 100
  for stock_code in stock_codes:
    print("stock:",stock_code)
    FFC.FLS.load_all_financial_one_stock(stock_code)
    FFC.FLS.load_all_processed_stock_basic_one_stock([stock_code])
    data_processed = FFC.financial_index_calc(stock_code)
    (row, colum) = data_processed.shape
    if(row<statistic_stock_min_len):
      statistic_stock_min_len = row
    statistic_stock_data[stock_code] = data_processed
    #plt.figure()
    #data_processed.plot.bar(data_processed.index)
  sum_data = statistic_stock_data[stock_codes[0]].iloc[-statistic_stock_min_len:,:]
  for stock_code in stock_codes[1:]:
    sum_data = sum_data + statistic_stock_data[stock_code].iloc[-statistic_stock_min_len:,:]
  pct_data = sum_data.pct_change(periods=4)
  pct_data.to_csv(store_path+'statistic_pct.csv');
  sum_data.to_csv(store_path+'statistic_sum.csv');
  #pct_data.plot.bar(pct_data.index)
  #plt.figure()
  #sum_data.plot.bar(sum_data.index)
if __name__ == '__main__':
  #stock_codes = ['000001','000002','000004']
  
  path = '../../../data/'
  main_financial_statistic_process(path)
  print("processed successfully!!!")
 # data_main = data[0]

