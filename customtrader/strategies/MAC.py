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
            
        #Iterates over the data and looks for trades
        def look_for_trade(self, row):
            #only save the max amount of data necessary
            if (len(self.data) == self.slow_ma_dp and self.slow_ma_dp != 0):
                self.data.pop(0)
                self.data.append(row)
                self.slow_ma = self.calculate_ma(self.slow_ma_dp)
                self.fast_ma = self.calculate_ma(self.fast_ma_dp)
                if (self.fast_ma > self.slow_ma and not self.in_position):
                    self.buy(row)
                elif(self.fast_ma < self.slow_ma and self.in_position):
                    self.sell(row)
            else: 
                self.data.append(row)

        def calculate_ma(self, ma):
            total_amount = 0.0
            for data_row in self.data[-ma:]:
                total_amount += float(data_row[4])
            return total_amount / ma
        
        def train_strategy(self, training_data):
            best_short_ma_period, best_long_ma_period, best_report = self.slow_ma, self.fast_ma, None

            for short_period in range(1, 30):
                for long_period in range(5, 100):
                    if short_period >= long_period:
                        continue

                    self.reset()
                    self.slow_ma_dp, self.fast_ma_dp = long_period, short_period
                    
                    report = self.train(training_data)
                    if best_report and self.evaluate_performance(report, best_report):
                        best_report = report
                        best_short_ma_period = short_period
                        best_long_ma_period = long_period
                    elif not best_report:
                        best_report = report

            print(f"best_long: {best_long_ma_period}")
            print(f"best_short: {best_short_ma_period}")

            self.reset()
            self.slow_ma_dp, self.fast_ma_dp = best_long_ma_period, best_short_ma_period
            return self
        
        def train(self, data):
            for row in data:
                self.look_for_trade(row)
                current_price = float(row[4])
                self.update_draw(current_price)

            if self.in_position:
                self.end_session()

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

