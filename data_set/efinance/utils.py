import efinance as ef

class ef_utils:
      
  def get_stock_codes(self):
    datacenter = ef.stock.datacenter()
    north_stock_status = datacenter.get_north_stock_status()
    stock_codes = sorted(north_stock_status['stock_code'].apply(lambda x: x[:-3]).values)
    return stock_codes
  
  def get_block_codes(block):
    push2_98_getter = ef.stock.push2_98_getter.push2_98()
    code_names = push2_98_getter.get_block_codes(block)
    return code_names.loc[:, 'stock_code'].values