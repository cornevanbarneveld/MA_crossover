import csv

class MA_crossover():
    def __init__(self, data_filename, trader, slow_ma, fast_ma):
        #get slow MA and fast MA from config or something
        self.slow_ma_dp = slow_ma
        self.fast_ma_dp = fast_ma
        self.data_filename = data_filename
        self.data = []
        self.slow_ma = 0
        self.fast_ma = 0
        self.in_position = False
        self.starting_amount = 1000
        self.trader = trader
    
    def look_for_trade(self):
        with open(self.data_filename, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)

            for row in csv_reader:
                #only save the max amount of data necessary
                if (len(self.data) == self.slow_ma_dp):
                    self.data.pop(0)
                    self.data.append(row)
                    self.slow_ma = self.calculate_ma(self.slow_ma_dp)
                    self.fast_ma = self.calculate_ma(self.fast_ma_dp)
                    
                    # print(f"MA: sma: {self.slow_ma} fma: {self.fast_ma}")
                    # if (self.fast_ma > self.slow_ma):
                    #     print("buy")
                    # elif(self.fast_ma < self.slow_ma):
                    #     print("sell")

                    if (self.fast_ma > self.slow_ma and self.in_position == False):
                        if (self.buy(row)):
                            self.in_position = True
                        
                    elif(self.fast_ma < self.slow_ma and self.in_position == True):
                        if (self.sell(row)):
                            self.in_position = False
                else: 
                    self.data.append(row)

    def calculate_ma(self, ma):
        total_amount = 0
        for i in range(0, ma):
            #add the closing price
            total_amount += float(self.data[i][4])
        return total_amount / ma
    
    def buy(self, latest_candle):
        #try to fullfil order 3 times?
        #do buy logic
        return self.trader.buy(latest_candle)

    def sell(self, latest_candle):
        #try to fullfill order 3 times?
        return self.trader.sell(latest_candle)

# class Live_trader():
#     def __init__(self):
#         pass

#     def buy():
#         pass

#     def sell():
#         pass

class Sample_trader():
    def __init__(self):
        self.starting_amount = 1000
        self.current_amount = self.starting_amount
        self.order_size_percent = 1
        self.bought_at = None
        self.oder_amount = 0

    def buy(self, latest_candle):
        self.bought_at = float(latest_candle[4])
        self.oder_amount = self.current_amount * self.order_size_percent
        self.current_amount -= self.current_amount * self.order_size_percent
        print(f"BUY: at: {self.bought_at}, amount: {self.oder_amount}, current amount: {self.current_amount}")
        return True

    def sell(self, latest_candle):
        sold_at = float(latest_candle[4]) 
        self.current_amount = sold_at / self.bought_at * self.oder_amount
        print(f"SELL: at: {sold_at}, current amount: {self.current_amount}")
        return True

