import csv

class Sample_trader():
    def __init__(self):
        self.starting_amount = 1000
        self.current_amount = self.starting_amount
        self.order_amount = 0
        self.order_size_percent = 1
        self.bought_at = None
        self.oder_amount = 0
        self.amount_of_trades = 0
        self.maximum_peak_perc = 0
        self.maximum_drawdown_perc = 0
        self.sharpe = 0
        self.wins = 0
        self.losses = 0
        self.winning_perc = 0
        self.losing_perc = 0
        self.risk_rew_ratio = 0
        self.avg_holding_period = 0
        self.benchmark_comparison = 0
        self.in_position = False

    def add_strategy(self, strategy):
        self.strategy = strategy

    def add_data(self, data_filename):
        self.data_filename = data_filename

    def run(self):
        with open(self.data_filename, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
  
            for row in csv_reader:
                self.strategy.look_for_trade(row)
                current_price = float(row[4])
                self.update_draw(current_price)

        print(f"Starting: Amount: {self.strategy.starting_amount}")
        print(f"Current: Amount: {self.strategy.current_amount}")
        print(f"Amount of trades: {self.strategy.amount_of_trades}")
        print(f"max peak percentage: {self.strategy.maximum_peak_perc}")
        print(f"max drawdown percentage: {self.strategy.maximum_drawdown_perc}")
        print(f"wins: {self.strategy.wins}")
        print(f"losses: {self.strategy.losses}")
        print(f"wins percentage: {self.strategy.winning_perc}")
        print(f"losses percentage: {self.strategy.losing_perc}")

    def update_draw(self, current_price):
        if self.strategy.in_position:
            draw_perc = (current_price / self.strategy.bought_at ) * 100 - 100
            if (draw_perc < self.strategy.maximum_drawdown_perc):
                self.strategy.maximum_drawdown_perc = draw_perc
            elif (draw_perc > self.strategy.maximum_peak_perc):
                self.strategy.maximum_peak_perc = draw_perc 
                
    def buy(self, latest_candle):
        self.bought_at = float(latest_candle[4])
        self.oder_amount = self.current_amount * self.order_size_percent
        self.order_amount = self.current_amount * self.order_size_percent
        self.current_amount -= self.order_amount
        # print(f"BUY: at: {self.bought_at}, amount: {self.oder_amount}, current amount: {self.current_amount}")
        self.in_position = True

    def sell(self, latest_candle):
        self.amount_of_trades += 1
        sold_at = float(latest_candle[4]) 
        new_amount = sold_at / self.bought_at * self.oder_amount
        self.calculate_wins_or_losses(new_amount)
        self.current_amount = new_amount
        # print(f"SELL: at: {sold_at}, current amount: {self.current_amount}")
        self.in_position = False


    def calculate_wins_or_losses(self, new_amount):
        if (new_amount > (self.current_amount + self.order_amount)):
            self.wins += 1
        elif (new_amount <= (self.current_amount + self.order_amount)):
            self.losses += 1

        self.winning_perc = self.wins / self.amount_of_trades * 100
        self.losing_perc = 100 - self.winning_perc

        