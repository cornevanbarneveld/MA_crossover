import customtrader.strategies.MAC as ma
import customtrader.candlestick_retriever as cr
import customtrader.Traders.live_trader as ltr
import customtrader.Traders.sample_trader as str
import customtrader.testers.monkey_trader as mktr
import customtrader.testers.backtester as btstr
import customtrader.testers.walk_foward_tester as wftr

if __name__ == '__main__':
   
    #MA_crossover
    # ma_c = ma.MA_crossover_factory(str.Sample_trader, 10, 2)
    ma_c = ma.MA_crossover_factory(str.Sample_trader, 19, 2)

    sample_trader = str.Sample_trader()

    sample_trader.add_strategy(ma_c)
    sample_trader.add_data('data/15minute.csv')
    
    backtester = btstr.Backtester(sample_trader, 'data/15minute.csv')
    monkey_trader = mktr.Monkey_trader(sample_trader, 'data/15minute.csv')
    walk_forward_tester = wftr.Walk_forward(sample_trader, 'data/15minute.csv', 4 , 8)
    walk_forward_tester.walk_forward_test()
    # backtester.run_backtest()
    # monkey_trader.run_monkey_test(50)

    # data = [
    #     'data/1month.csv',
    #     'data/1week.csv',
    #     'data/12hour.csv',
    #     'data/8hour.csv',
    #     'data/6hour.csv',
    #     'data/4hour.csv',
    #     'data/2hour.csv',
    #     'data/1hour.csv',
    #     'data/30minute.csv',
    #     'data/15minute.csv',
    #     'data/5minute.csv',
    #     'data/3minute.csv',
    #     'data/1minute.csv'
    # ]

    # for datafile in data:
    #     sample_trader.add_data(datafile)
    #     print(f"DATA: {datafile}----------------------------------------------------------")
    #     sample_trader.run_backtest()
    #     sample_trader.reset()
    #     sample_trader.run_monkey_test()
    #     sample_trader.reset()

    #retrieve live candlesticks
    # cr.CandlestickWebSocketApp(30)   