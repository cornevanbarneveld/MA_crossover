from ..Traders import live_trader
import pandas as pd
import numpy as np

def MACD_factory(parent_class, interval, symbol):

    class MACD(parent_class):
        def __init__(self):
            #get slow MA and fast MA from config or something
            super().__init__()
            self.current_macd = 0
            self.current_signal = 0
            self.data = []
            self.interval = interval
            self.symbol = symbol
            
        #Iterates over the data and looks for trades
        def look_for_trade(self, row):
            #only save the max amount of data necessary
            if (len(self.data) == 26):
                self.data.pop(0)
                self.data.append(row)
                self.current_macd, self.current_signal = self.calculate_macd_signal(self.data)
                if (self.current_macd > self.current_signal and not self.in_position):
                    self.buy(row)
                elif(self.current_macd < self.current_signal and self.in_position):
                    self.sell(row)
            else: 
                if isinstance(live_trader.Live_trader(), parent_class):
                    self.data = self.fill_data(26)
                else:
                    self.data.append(row)

        def calculate_macd_signal(self, candlesticks, short_window=12, long_window=26, signal_window=9):
            # Convert the list of candlesticks to a NumPy array
            data_array = np.array(candlesticks, dtype=np.float64)

            # Extract the relevant columns
            close = data_array[:, 4]

            # Calculate the short-term and long-term Exponential Moving Averages
            short_ema = pd.Series(close).ewm(span=short_window, adjust=False).mean().values
            long_ema = pd.Series(close).ewm(span=long_window, adjust=False).mean().values

            # Calculate the MACD line (DIF)
            macd_line = short_ema - long_ema

            # Calculate the Signal Line (DEA)
            signal_line = pd.Series(macd_line).ewm(span=signal_window, adjust=False).mean().values

            # Return the current values of MACD and Signal Line
            current_macd = macd_line[-1]
            current_signal = signal_line[-1]

            return current_macd, current_signal

    return MACD()

