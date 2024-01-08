from ..Traders import live_trader

def Positive_Candle_Momentum_factory(parent_class, interval, symbol, trade_percentage):

    class PCM(parent_class):
        def __init__(self):
            super().__init__()
            self.interval = interval
            self.symbol = symbol
            self.trade_percentage = trade_percentage
            
 
        def look_for_trade(self, row):
            if self.in_position:
                self.sell(row)
                # self.buy(row)
            else:
                opening_price = float(row[1])
                closing_price = float(row[4])

                if opening_price > closing_price:

                    highest_price = float(row[2])
                    lowest_price = float(row[3])
                
                    candle_length = highest_price - lowest_price
                    bottom_wick = closing_price - lowest_price
                    if bottom_wick != 0:
                        differ_percentage =  (bottom_wick / candle_length) * 100

                        if differ_percentage > trade_percentage:
                            self.buy(row)
                            # self.sell(row)

    return PCM()

