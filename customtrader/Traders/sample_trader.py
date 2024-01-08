import csv
from ..loggers import test_report

class Sample_trader():
    def __init__(self):
        self.starting_amount = 1000
        self.current_amount = self.starting_amount
        self.order_amount = 0
        self.order_size_percent = 1
        self.bought_at = None
        self.amount_of_trades = 0
        self.maximum_peak_perc = 0
        self.maximum_drawdown_perc = 0
        self.sharpe = 0
        self.wins = 0
        self.losses = 0
        self.risk_rew_ratio = 0
        self.avg_holding_period = 0
        self.benchmark_comparison = 0
        self.in_position = False
        self.max_wait = 0

    def reset(self):
        self.starting_amount = 1000
        self.current_amount = self.starting_amount
        self.order_amount = 0
        self.order_size_percent = 1
        self.bought_at = None
        self.amount_of_trades = 0
        self.maximum_peak_perc = 0
        self.maximum_drawdown_perc = 0
        self.sharpe = 0
        self.wins = 0
        self.losses = 0
        self.risk_rew_ratio = 0
        self.avg_holding_period = 0
        self.benchmark_comparison = 0
        self.in_position = False
        self.max_wait = 0
        self.slow_ma = 0
        self.fast_ma = 0
        self.data = []

    def add_strategy(self, strategy):
        self.strategy = strategy

    def add_data(self, data_filename):
        self.data_filename = data_filename

    def generate_report(self):
        return test_report.Test_Report(self.starting_amount, 
                                       self.current_amount,
                                       self.amount_of_trades,
                                       self.maximum_peak_perc,
                                       self.maximum_drawdown_perc,
                                       None,
                                       self.wins,
                                       self.losses,
                                       self.winning_perc,
                                       self.losing_perc,
                                       None,
                                       None,
                                       self.benchmark_comparison)
    
    def print_report(self):
        self.generate_report().print_report()

    def calculate_benchmark(self, starting_price, ending_price):
        self.benchmark_comparison = ending_price / starting_price * self.starting_amount

    def update_draw(self, current_price):
        if self.in_position:

            draw_perc = (current_price / self.bought_at ) * 100 - 100
            print(f"current_price: {current_price}" )
            print(f"self.bought_at: {self.bought_at}" )
            print(f"draw perc: {draw_perc}" )
            print(f"draw perc: {draw_perc}" )
            print(f"draw perc: {draw_perc}" )
            if (draw_perc < self.maximum_drawdown_perc):
                self.maximum_drawdown_perc = draw_perc
            elif (draw_perc > self.maximum_peak_perc):
                self.maximum_peak_perc = draw_perc 
                
    def buy(self, latest_candle):
        self.bought_at = float(latest_candle[4])
        self.order_amount = self.current_amount * self.order_size_percent
        self.current_amount -= self.order_amount
        self.in_position = True

    def sell(self, latest_candle):
        self.amount_of_trades += 1
        sold_at = float(latest_candle[4]) 
        new_amount = sold_at / self.bought_at * self.order_amount
        self.calculate_wins_or_losses(new_amount)
        self.current_amount = new_amount
        self.in_position = False
        
    def end_session(self):
        self.current_amount += self.order_amount
        self.in_position = False

    def calculate_wins_or_losses(self, new_amount):
        if (new_amount > (self.current_amount + self.order_amount)):
            self.wins += 1
        elif (new_amount <= (self.current_amount + self.order_amount)):
            self.losses += 1

    @property
    def winning_perc(self):
        if self.wins == 0 or self.amount_of_trades == 0:
            return 0
        return self.wins / self.amount_of_trades * 100

    @property
    def losing_perc(self):
        if self.winning_perc == 0:
            return 0
        return 100 - self.winning_perc