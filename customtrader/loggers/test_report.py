class Test_Report():
    def __init__(self, starting_amount,
        current_amount,
        amount_of_trades,
        maximum_peak_perc,
        maximum_drawdown_perc,
        sharpe,
        wins,
        losses,
        winning_perc,
        losing_perc,
        risk_rew_ratio,
        avg_holding_period,
        benchmark_comparison
    ):
        self.starting_amount = starting_amount
        self.current_amount = current_amount
        self.amount_of_trades = amount_of_trades
        self.maximum_peak_perc = maximum_peak_perc
        self.maximum_drawdown_perc = maximum_drawdown_perc
        self.sharpe = sharpe
        self.wins = wins
        self.losses = losses
        self.winning_perc = winning_perc
        self.losing_perc = losing_perc
        self.risk_rew_ratio = risk_rew_ratio
        self.avg_holding_period = avg_holding_period
        self.benchmark_comparison = benchmark_comparison

    # Getter for field1
    def update(
        self,
        starting_amount,
        current_amount,
        amount_of_trades,
        maximum_peak_perc,
        maximum_drawdown_perc,
        sharpe,
        wins,
        losses,
        winning_perc,
        losing_perc,
        risk_rew_ratio,
        avg_holding_period,
        benchmark_comparison
    ):
        
        self.starting_amount = starting_amount
        self.current_amount = current_amount
        self.amount_of_trades = amount_of_trades
        self.maximum_peak_perc = maximum_peak_perc
        self.maximum_drawdown_perc = maximum_drawdown_perc
        self.sharpe = sharpe
        self.wins = wins
        self.losses = losses
        self.winning_perc = winning_perc
        self.losing_perc = losing_perc
        self.risk_rew_ratio = risk_rew_ratio
        self.avg_holding_period = avg_holding_period
        self.benchmark_comparison = benchmark_comparison

    def print_report(self):
        print(" ")
        print("REPORT-START-------------------------------------------------")
        print(f"Starting Amount: {self.starting_amount}")
        print(f"Current Amount: {self.current_amount}")
        print(f"Amount of trades: {self.amount_of_trades}")
        print(f"max peak percentage: {self.maximum_peak_perc}")
        print(f"max drawdown percentage: {self.maximum_drawdown_perc}")
        print(f"wins: {self.wins}")
        print(f"losses: {self.losses}")
        print(f"wins percentage: {self.winning_perc}")
        print(f"losses percentage: {self.losing_perc}")
        print(f"benchmark comparison: {self.benchmark_comparison}")
        print("REPORT-END-----------------------------------------------------")
        print(" ")
    