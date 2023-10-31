import customtrader.strategies.MAC as ma
import customtrader.candlestick_retriever as cr
import customtrader.Traders.live_trader as ltr
import customtrader.Traders.sample_trader as str


if __name__ == '__main__':
   
    #MA_crossover
    ma_c = ma.MA_crossover_factory(str.Sample_trader, 10, 2)
    
    sample_trader = str.Sample_trader()
    sample_trader.add_strategy(ma_c)
    sample_trader.add_data('data/1day.csv')
    sample_trader.run()

    #retrieve live candlesticks
    # cr.CandlestickWebSocketApp(30)   