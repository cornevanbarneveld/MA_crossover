import customtrader.strategies.MAC as ma
import customtrader.candlestick_retriever as cr

if __name__ == '__main__':
   
    #MA_crossover
    ma_c = ma.MA_crossover('data/1day.csv', 10, 2)
    ma_c.look_for_trade()

    #retrieve live candlesticks
    # cr.CandlestickWebSocketApp(30)   