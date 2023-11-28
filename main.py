import customtrader.strategies.MAC as ma
import customtrader.candlestick_retriever as cr
import customtrader.Traders.live_trader as ltr
import customtrader.Traders.sample_trader as str
import customtrader.testers.monkey_trader as mktr
import customtrader.testers.backtester as btstr
import customtrader.testers.walk_foward_tester as wftr

if __name__ == '__main__':
   
#     #MA_crossover
    ma_c = ma.MA_crossover_factory(str.Sample_trader, 50, 20)
    # ma_c = ma.MA_crossover_factory(ltr.Live_trader, 11, 4)

    #Live trader
    # live_trader = ltr.Live_trader()
    # live_trader.set_symbol(symbol="BTC")
    # live_trader.add_strategy(ma_c)

    sample_trader = str.Sample_trader()
    sample_trader.add_strategy(ma_c)
    
#     #backtest
    backtester = btstr.Backtester(sample_trader, 'data/1hour.csv')    
    backtester.run_backtest()

#     #monkey_test
#     # monkey_trader = mktr.Monkey_trader(sample_trader, 'data/15minute.csv')
#     # monkey_trader.run_monkey_test(50)
 

#     #walk forward
    # walk_forward_tester = wftr.Walk_forward(sample_trader, 'data/15minute.csv', 4 , 8)
    # walk_forward_tester.walk_forward_test_anchored()
#     # walk_forward_tester.walk_forward_test_un_anchored()




    # retrieve live candlesticks
    # cr.CandlestickWebSocketApp(30, live_trader)   
    # live_trader.get_current_positions()


