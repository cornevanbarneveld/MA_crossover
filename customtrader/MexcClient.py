import time
import config
import requests
import time
import hashlib
import hmac

class MEXC_client():

    def __init__(self):
        self.url = "https://api.mexc.com/api/v3"
        self.headers = {
            "X-MEXC-APIKEY": config.API_KEY,
            "Content-Type": "application/json", 
        }

    def buy(self, symbol, type, quote_order_qty):
        timestamp = int(time.time() * 1000)  # Current timestamp in milliseconds
        side = "BUY"
        data_string = f"quoteOrderQty={quote_order_qty}&recvWindow=5000&side={side}&symbol={symbol}&timestamp={timestamp}&type={type}"
        signature = self.create_signature(data_string)
        url = f"{self.url}/order?&quoteOrderQty={quote_order_qty}&recvWindow=5000&side={side}&symbol={symbol}&timestamp={timestamp}&type={type}&signature={signature}"

        try:
            response = requests.post(url, headers=self.headers)
            # Print the response
            print(response.json())
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

    def sell(self, symbol, type, quantity):
        timestamp = int(time.time() * 1000)  # Current timestamp in milliseconds
        side = "SELL"
        data_string = f"quantity={quantity}&recvWindow=5000&side={side}&symbol={symbol}&timestamp={timestamp}&type={type}"
        signature = self.create_signature(data_string)
        url = f"{self.url}/order?&quantity={quantity}&recvWindow=5000&side={side}&symbol={symbol}&timestamp={timestamp}&type={type}&signature={signature}"

        try:
            response = requests.post(url, headers=self.headers)
            # Print the response
            print(response.json())
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

    def get_current_positions(self):
        timestamp = int(time.time() * 1000)  # Current timestamp in milliseconds
        data_string = f"timestamp={timestamp}"
        signature = self.create_signature(data_string)
        url = f"{self.url}/account?timestamp={timestamp}&signature={signature}"

        try:
            response = requests.get(url, headers=self.headers)
            # Print the response
            response_data = response.json()
            return response_data['balances']
            
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

        # impl throwing exception
        return []
    
    def create_signature(self, data_string):
        return hmac.new(config.SECRET_KEY.encode('utf-8'), data_string.encode('utf-8'), hashlib.sha256).hexdigest()

    def get_historical_data(self, symbol, interval, candles):
        timestamp = int(time.time() * 1000)  # Current timestamp in milliseconds
        url = f"{self.url}/klines?symbol={symbol}&interval={interval}&startTime={timestamp}"

        try:
            response = requests.get(url, headers=self.headers)
            # Print the response
            response_data = response.json()
            return response_data[-candles:]
            
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

        # impl throwing exception
        return []

    
