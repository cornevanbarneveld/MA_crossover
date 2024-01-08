import csv
from datetime import datetime


class Backtester():
    def __init__(self, trader, filename, start_date, end_date):
        self.trader = trader
        self.data_filename = filename
        self.start_date = start_date
        self.end_date = end_date

    def run_backtest(self):
        with open(self.data_filename, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)

            first_line = next(csv_reader, None)

            last_line = None
            for row in csv_reader:
                timestamp = float(row[0])
                date = datetime.utcfromtimestamp(timestamp)
                if self.start_date <= date <= self.end_date:
                    self.trader.strategy.look_for_trade(row)
                    current_price = float(row[4])
                    self.trader.strategy.update_draw(current_price)
                    last_line = row
            if (first_line != None and last_line != None):
                self.trader.strategy.calculate_benchmark(float(first_line[4]), float(last_line[4]))

        if self.trader.strategy.in_position:
            self.trader.strategy.end_session()

        self.trader.strategy.print_report()
