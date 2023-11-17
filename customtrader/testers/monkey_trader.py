import csv
import random
from ..loggers import test_report
 

class Monkey_trader():
    def __init__(self, trader, filename):
        self.trader = trader
        self.data_filename = filename

    def run_monkey_test(self, amount):
        self.trader.max_wait = self.calculate_max_trade_wait()
        self.monkey_test_reports_buy = []
        self.monkey_test_reports_sell = []
        self.monkey_test_reports_buy_and_sell = []

        for i in range(amount):
            self.monkey_test_reports_buy.append(self.random_buy())
            print("random_buy")
            self.trader.print_report()

            self.monkey_test_reports_sell.append(self.random_sell())
            print("random_sell")
            self.trader.print_report()

            self.monkey_test_reports_buy_and_sell.append(self.random_buy_and_sell())
            print("random_sell_and_buy")
            self.trader.print_report()

        self.calucalte_averages(self.monkey_test_reports_buy).print_report()
        self.calucalte_averages(self.monkey_test_reports_sell).print_report()
        self.calucalte_averages(self.monkey_test_reports_buy_and_sell).print_report()

    def calucalte_averages(self, reports):
        total_reports = len(reports)

        if total_reports == 0:
            return None  # Avoid division by zero

        current_amount = 0
        amount_of_trades = 0
        maximum_peak_perc = 0
        maximum_drawdown_perc = 0
        wins = 0
        losses = 0
        winning_perc = 0
        losing_perc = 0

        for i, report in enumerate(reports):
            weight = i + 1
            current_amount = (i * current_amount + report.current_amount) / weight
            amount_of_trades = (i * amount_of_trades + report.amount_of_trades) / weight
            maximum_peak_perc = (i * maximum_peak_perc + report.maximum_peak_perc) / weight
            maximum_drawdown_perc = (i * maximum_drawdown_perc + report.maximum_drawdown_perc) / weight
            wins = (i * wins + report.wins) / weight
            losses = (i * losses + report.losses) / weight
            winning_perc = (i * winning_perc + report.winning_perc) / weight
            losing_perc = (i * losing_perc + report.losing_perc) / weight

        return test_report.Test_Report(None, 
                                       current_amount,
                                       amount_of_trades,
                                       maximum_peak_perc,
                                       maximum_drawdown_perc,
                                       None,
                                       wins,
                                       losses,
                                       winning_perc,
                                       losing_perc,
                                       None,
                                       None,
                                       None)
    



    def calculate_max_trade_wait(self):
        with open(self.data_filename, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)

            count = 0
            highest_count = 0
            shortest_count = -1
            for row in csv_reader: 
                #
                position = self.trader.in_position
                #
                self.trader.strategy.look_for_trade(row)
                
                if position != self.trader.in_position:
                    if count > highest_count:
                        highest_count = count
                    if shortest_count == -1:
                        shortest_count = count
                    if count < shortest_count:
                        shortest_count = count
                else: 
                    count += 1
                
            return highest_count - shortest_count

    def random_sell(self):
        with open(self.data_filename, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)

            first_line = next(csv_reader, None)

            last_line = None
            sellpoint = 0
            count = 0
            for row in csv_reader: 
                if self.trader.strategy.in_position:
                    if sellpoint == 0:
                        sellpoint = random.randint(1, 100)
                    count += 1
                    if count == sellpoint:
                        self.trader.strategy.sell(row)
                        sellpoint = 0
                        count = 0
                
                self.trader.strategy.look_for_trade(row)
                current_price = float(row[4])
                self.trader.update_draw(current_price)
                last_line = row

            self.trader.calculate_benchmark(float(first_line[4]), float(last_line[4]))

        if self.trader.strategy.in_position:
            self.trader.strategy.end_session()
        
        return self.trader.generate_report()

    def random_buy_and_sell(self):
        with open(self.data_filename, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)

            first_line = next(csv_reader, None)

            last_line = None
            tradepoint = 0
            count = 0
            for row in csv_reader: 
                if tradepoint == 0:
                    tradepoint = random.randint(1, 100)
                count += 1
                if count == tradepoint:
                    if self.trader.strategy.in_position:

                        self.trader.strategy.sell(row)
                    else:
                        self.trader.strategy.buy(row)
                    tradepoint = 0
                    count = 0
                
                current_price = float(row[4])
                self.trader.update_draw(current_price)
                last_line = row

            self.trader.calculate_benchmark(float(first_line[4]), float(last_line[4]))

        if self.trader.strategy.in_position:
            self.trader.strategy.end_session()
        
        return self.trader.generate_report()


    def random_buy(self):
        with open(self.data_filename, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)

            first_line = next(csv_reader, None)

            last_line = None
            buypoint = 0
            count = 0
            for row in csv_reader: 
                if self.trader.strategy.in_position == False:
                    if buypoint == 0:
                        buypoint = random.randint(1, 100)
                    count += 1
                    if count == buypoint:
                        self.trader.strategy.buy(row)
                        buypoint = 0
                        count = 0
                
                self.trader.strategy.look_for_trade(row)
                current_price = float(row[4])
                self.trader.update_draw(current_price)
                last_line = row

            self.trader.calculate_benchmark(float(first_line[4]), float(last_line[4]))

        if self.trader.strategy.in_position:
            self.trader.strategy.end_session()
        
        return self.trader.generate_report()
