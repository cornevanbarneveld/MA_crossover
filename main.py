import customtrader.strategies.MAC as ma

if __name__ == '__main__':
   st = ma.Sample_trader()
   ma_c = ma.MA_crossover('data/1day.csv', st, 10, 2)
   ma_c.look_for_trade()