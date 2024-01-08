import customtrader.strategies.RMAC as rma
import customtrader.strategies.MAC as ma
import customtrader.strategies.MACD as macd
import customtrader.strategies.PCM as pcm

import customtrader.candlestick_retriever as cr

import customtrader.Traders.live_trader as ltr
import customtrader.Traders.sample_trader as str

import customtrader.testers.monkey_trader as mktr
import customtrader.testers.backtester as btstr
import customtrader.testers.walk_foward_tester as wftr

from datetime import datetime

# if __name__ == '__main__':
   
#     #MA_crossover
#     ma_c = rma.RMA_crossover_factory(ltr.Live_trader, 11, 4, "1m", "BTCUSDC")

#     #Live trader
#     live_trader = ltr.Live_trader()
#     live_trader.add_strategy(ma_c)

#     # retrieve live candlesticks
#     cr.CandlestickWebSocketApp(12, live_trader)   

if __name__ == '__main__':
   
    # MA_crossovers
    # strategy = rma.RMA_crossover_factory(str.Sample_trader, 11, 4, "1m", "BTCUSDC")
    strategy = ma.MA_crossover_factory(str.Sample_trader, 11, 4, "15m", "BTCUSDC")
    # strategy = macd.MACD_factory(str.Sample_trader, "15m", "BTCUSDC")
    # strategy = pcm.Positive_Candle_Momentum_factory(str.Sample_trader, "15m", "BTCUSDC", 50)

    # sample trader
    sample_trader = str.Sample_trader()
    sample_trader.add_strategy(strategy)
    
    #first possible: Thursday, 8 17, 2017 4:00:59.999 AM
    #last possible: Tuesday, 6 27, 2023 5:11:59.999 PM
    start_date = datetime(2022, 1, 17)
    end_date = datetime(2023, 6, 27)

    # backtest
    backtester = btstr.Backtester(sample_trader, 'data/15minute.csv', start_date, end_date)    
    backtester.run_backtest()

    # monkey_test
    # monkey_trader = mktr.Monkey_trader(sample_trader, 'data/15minute.csv')
    # monkey_trader.run_monkey_test(50)
 
    # walk forward
    # walk_forward_tester = wftr.Walk_forward(sample_trader, 'data/1minute.csv', 4 , 8)
    # walk_forward_tester.walk_forward_test_anchored()
    # walk_forward_tester.walk_forward_test_un_anchored()

   
