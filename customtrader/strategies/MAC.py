def MA_crossover_factory(parent_class, slow_ma, fast_ma):

    class MA_crossover(parent_class):
        def __init__(self):
            #get slow MA and fast MA from config or something
            super().__init__()
            self.slow_ma_dp = slow_ma
            self.fast_ma_dp = fast_ma
            self.data = []
            self.slow_ma = 0
            self.fast_ma = 0
            self.starting_amount = 1000
        
        #Iterates over the data and looks for trades
        def look_for_trade(self, row):
            #only save the max amount of data necessary
            if (len(self.data) == self.slow_ma_dp):
                self.data.pop(0)
                self.data.append(row)
                self.slow_ma = self.calculate_ma(self.slow_ma_dp)
                self.fast_ma = self.calculate_ma(self.fast_ma_dp)

                if (self.fast_ma > self.slow_ma and self.in_position == False):
                    self.buy(row)
                        
                elif(self.fast_ma < self.slow_ma and self.in_position == True):
                    self.sell(row)
            else: 
                self.data.append(row)

        def calculate_ma(self, ma):
            total_amount = 0
            for i in range(0, ma):
                #add the closing price
                total_amount += float(self.data[i][4])
            return total_amount / ma
        
        
    return MA_crossover()

