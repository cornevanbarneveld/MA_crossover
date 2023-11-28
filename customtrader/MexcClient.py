import time
import config
import requests
import time
import hashlib
import hmac
from pymexc import spot


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

    
# if __name__ == '__main__':
#     endpoint = "https://api.mexc.com/api/v3/order/test"
#     symbol = "BTCUSDC"
#     side = "BUY"
#     type = "MARKET"
#     quantity = 0.000255
#     quote_order_qty = 10
#     # price = 0.0001
#     timestamp = int(time.time() * 1000)  # Current timestamp in milliseconds

#     # quoteOrderQty=10&recvWindow=5000&side=BUY&symbol=BTCUSDC&timestamp=1700594753821&type=MARKET
#     # quoteOrderQty=10&recvWindow=5000&side=BUY&symbol=BTCUSDC&timestamp=1700595648335&type=MARKET&signature=e0c4d12f7f1b20ed35ddaee0d32de8b6eff5988fd72b014475ff4edb190b7e30


#     # Create the signature
#     data = f"quoteOrderQty={quote_order_qty}&recvWindow=5000&side={side}&symbol={symbol}&timestamp={timestamp}&type={type}"
#     print(data)
#     signature = hmac.new(config.SECRET_KEY.encode('utf-8'), data.encode('utf-8'), hashlib.sha256).hexdigest()
#     print(signature)
#     # Build the request URL
#     url = f"{endpoint}?&quoteOrderQty={quote_order_qty}&recvWindow=5000&side={side}&symbol={symbol}&timestamp={timestamp}&type={type}&signature={signature}"
#     print(url)
    
#     headers = {
#         "X-MEXC-APIKEY": config.API_KEY,
#         "Content-Type": "application/json",  # Adjust as needed
#     }

#     # Make the API request
#     try:
#         response = requests.post(url, headers=headers)
#         # Print the response
#         print(response)
#         print(response.json())

#     except requests.exceptions.RequestException as e:
#         print(f"Error: {e}")



    spot_client = spot.HTTP(api_key = config.API_KEY, api_secret = config.SECRET_KEY)


#     # print(spot_client.account_information())
#     # print(spot_client.exchange_info(
#     #     symbols=["BTCUSDC"]))
#     # print(spot_client.get_currency_info())
#     # print(spot_client.order_book(symbol))
#     # try:
#     #     response = spot_client.new_order(
#     #         symbol=symbol,
#     #         side=side,
#     #         order_type=type,
#     #         quantity=quantity
#     #     )

#     #     print(response)

#     # try:
#     #     response = spot_client.new_order(
#     #         symbol=symbol,
#     #         side=side,
#     #         order_type=type,
#     #         quote_order_qty=quote_order_qty)
#     #     # print(spot_client.get_currency_info())
#     # except MexcAPIError as e:
#     #     print(f"Error: {repr(e)}")
#     #     print(f"Error Message: {e.message.decode('utf-8')}")

#     # except Exception as e:
#     #     print(f"Error: {e}")



