import csv
import math

class Walk_forward():
    def __init__(self, trader, filename, window_size_in_steps, max_steps):
        self.trader = trader
        self.data_filename = filename
        self.window_size = window_size_in_steps
        self.step = max_steps

        
    def walk_forward_test(self):
        with open(self.data_filename, 'r') as csv_file:
            csv_reader = list(csv.reader(csv_file))
            row_count = len(csv_reader)
            lines_for_step = math.floor(row_count / self.step)
            current_amount_of_steps = lines_for_step

            window_data = []
            step_data = [] 

            reports = []
            print("open")
            for i, row in enumerate(csv_reader):
                if i > current_amount_of_steps:
                    current_amount_of_steps += lines_for_step
                    window_data.append(step_data)
                    step_data = []
                    
                step_data.append(row)
                if len(window_data) == self.window_size:
                    print("wf test")
                    train_data = []
                    for sublist in window_data[:-1]:
                        train_data.extend(sublist)
                    best_strategy = self.trader.strategy.train_strategy(train_data)
                    self.trader.reset()
                    self.trader.add_strategy(best_strategy)

                    print("test_test")
                    # Test the strategy on the test data
                    for test_row in window_data[-1]:
                        self.trader.strategy.look_for_trade(test_row)
                        current_price = float(test_row[4])
                        self.trader.strategy.update_draw(current_price)

                    reports.append(self.trader.strategy.generate_report())
                    self.trader.strategy.print_report()
                    window_data.pop(0)

            
            
                


