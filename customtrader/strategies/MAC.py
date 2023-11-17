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
        
        def train_strategy(self, training_data):
            best_short_ma_period = self.slow_ma
            best_long_ma_period = self.fast_ma
            best_report = None

            for short_period in range(1, 5):
                for long_period in range(5, 10):
                    # cloned_strategy = MA_crossover_factory(parent_class, short_period, long_period)
                    print(short_period)
                    print(long_period)

                    self.reset()
                    # self.add_strategy(cloned_strategy)
                    self.slow_ma = 0
                    self.fast_ma = 0
                    self.data = []
                    self.fast_ma_dp = short_period
                    self.slow_ma_dp = long_period
                    report = self.train(training_data)
                    
                    if best_report != None:
                        if self.evaluate_performance(report, best_report):
                            best_report = report
                            best_short_ma_period = short_period
                            best_long_ma_period = long_period
                    else:
                        best_report = report

            print(best_long_ma_period)
            print(best_short_ma_period)

            return self

        def train(self, data):
            for row in data:
                self.look_for_trade(row)
                current_price = float(row[4])
                self.update_draw(current_price)

            if self.in_position:
                self.end_session()

            self.print_report()
            return self.generate_report()

        def evaluate_performance(self, report, best_report):
            score = 0
            if report.current_amount >= best_report.current_amount:
                score += 5

            if report.maximum_drawdown_perc <= best_report.maximum_drawdown_perc:
                score += 2

            if report.winning_perc >=  best_report.winning_perc:
                score += 2

            return score == 9 or score == 7

        
    return MA_crossover()

