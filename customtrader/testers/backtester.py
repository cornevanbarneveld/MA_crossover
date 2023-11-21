import csv

class Backtester():
    def __init__(self, trader, filename):
        self.trader = trader
        self.data_filename = filename

    def run_backtest(self):
        with open(self.data_filename, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)

            first_line = next(csv_reader, None)

            last_line = None
            for row in csv_reader:
                in_pos = self.trader.strategy.in_position

                self.trader.strategy.look_for_trade(row)
                current_price = float(row[4])
                self.trader.strategy.update_draw(current_price)
                last_line = row

                # if in_pos != self.trader.strategy.in_position and self.trader.strategy.in_position == False:
                #     self.trader.strategy.print_report()

            self.trader.strategy.calculate_benchmark(float(first_line[4]), float(last_line[4]))

        if self.trader.strategy.in_position:
            self.trader.strategy.end_session()

        self.trader.strategy.print_report()
