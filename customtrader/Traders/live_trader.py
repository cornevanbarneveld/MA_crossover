from ..loggers import test_report
from .. import MexcClient

class Live_trader():
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
        self.client = MexcClient.MEXC_client()

    def get_current_positions(self, symbol):
        current_positions = self.client.get_current_positions()
        print(current_positions)
        self.position_amount = None
        self.spot_amount = None
        for balance in current_positions:
            if balance['asset'] == 'USDC':
                self.spot_amount = float(balance['free'])
            elif balance['asset'] == symbol:
                self.position_amount = float(balance['free'])
        
        print(self.spot_amount)
        print(self.position_amount)

    def fill_data(self, candles):
        print(self.client.get_historical_data(self.symbol, self.interval, candles))
        return self.client.get_historical_data(self.symbol, self.interval, candles)
        # return self.client.get_historical_data(self.symbol, )

    def add_strategy(self, strategy):
        self.strategy = strategy

    def look_for_trade(self, datapoint):
        self.strategy.look_for_trade(datapoint)

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
        # retrieve latest order data
        self.in_position = True
        self.get_current_positions("BTC")
        print("Buy")
        #impl buy  
        self.client.buy("BTCUSDC", "MARKET", self.spot_amount)
    

    def sell(self, latest_candle):
        sold_at = float(latest_candle[4]) 
        #retrieve latest order data
        self.in_position = False
        self.get_current_positions("BTC")
        print("sell")
        #impl sell
        self.client.sell("BTCUSDC", "MARKET", self.position_amount)

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