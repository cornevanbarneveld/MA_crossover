import csv
from ..loggers import test_report
import config
import requests
import time
import hashlib
import hmac

class Sample_trader():
    def __init__(self):
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

    def get_current_amount(self):
        self.spot_amount = None
        self.current_position = None
        #implement retrieving current position

    def add_strategy(self, strategy):
        self.strategy = strategy

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
            if (draw_perc < self.maximum_drawdown_perc):
                self.maximum_drawdown_perc = draw_perc
            elif (draw_perc > self.maximum_peak_perc):
                self.maximum_peak_perc = draw_perc 
                
    def buy(self, latest_candle):
        self.bought_at = float(latest_candle[4])
        self.order_amount = self.current_amount * self.order_size_percent
        self.current_amount -= self.order_amount
        self.in_position = True

        endpoint = "https://api.example.com/api/v3/order"
        symbol = "BTCUSDT"
        side = "BUY"
        type = "MARKET"
        quantity = 1
        price = 0.000001
        timestamp = int(time.time() * 1000)  # Current timestamp in milliseconds

        # Create the signature
        data = f"symbol={symbol}&side={side}&type={type}&quantity={quantity}&price={price}&timestamp={timestamp}"
        signature = hmac.new(config.SECRET_KEY.encode(), data.encode(), hashlib.sha256).hexdigest()

        # Build the request URL
        url = f"{endpoint}?symbol={symbol}&side={side}&type={type}&quantity={quantity}&price={price}&timestamp={timestamp}&signature={signature}"

        # Make the API request
        response = requests.post(url, headers={"X-MBX-APIKEY": config.API_KEY})

        # Print the response
        print(response.json())


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