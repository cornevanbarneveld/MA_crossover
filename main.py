import customtrader.strategies.MAC as ma
import customtrader.candlestick_retriever as cr
import customtrader.Traders.live_trader as ltr
import customtrader.Traders.sample_trader as str
import customtrader.testers.monkey_trader as mktr
import customtrader.testers.backtester as btstr
import customtrader.testers.walk_foward_tester as wftr
import config
import requests
import time
import hashlib
import hmac
from pymexc import spot
from pymexc.base import MexcAPIError
import json

# if __name__ == '__main__':
   
#     #MA_crossover
#     # ma_c = ma.MA_crossover_factory(str.Sample_trader, 10, 2)
#     ma_c = ma.MA_crossover_factory(str.Sample_trader, 11, 4)

#     sample_trader = str.Sample_trader()
#     sample_trader.add_strategy(ma_c)
#     sample_trader.add_data('data/15minute.csv')
    
#     #backtest
#     backtester = btstr.Backtester(sample_trader, 'data/15minute.csv')    
#     backtester.run_backtest()

#     #monkey_test
#     # monkey_trader = mktr.Monkey_trader(sample_trader, 'data/15minute.csv')
#     # monkey_trader.run_monkey_test(50)


#     #walk forward
#     # walk_forward_tester = wftr.Walk_forward(sample_trader, 'data/15minute.csv', 4 , 8)
#     # walk_forward_tester.walk_forward_test_anchored()
#     # walk_forward_tester.walk_forward_test_un_anchored()


#     # data = [
#     #     'data/1month.csv',
#     #     'data/1week.csv',
#     #     'data/12hour.csv',
#     #     'data/8hour.csv',
#     #     'data/6hour.csv',
#     #     'data/4hour.csv',
#     #     'data/2hour.csv',
#     #     'data/1hour.csv',
#     #     'data/30minute.csv',
#     #     'data/15minute.csv',
#     #     'data/5minute.csv',
#     #     'data/3minute.csv',
#     #     'data/1minute.csv'
#     # ]

#     # for datafile in data:
#     #     sample_trader.add_data(datafile)
#     #     print(f"DATA: {datafile}----------------------------------------------------------")
#     #     sample_trader.run_backtest()
#     #     sample_trader.reset()
#     #     sample_trader.run_monkey_test()
#     #     sample_trader.reset()

#     #retrieve live candlesticks
#     # cr.CandlestickWebSocketApp(30)   

if __name__ == '__main__':
    endpoint = "https://api.mexc.com/api/v3/order"
    symbol = "BTCUSDC"
    side = "BUY"
    type = "MARKET"
    quantity = 0.000255
    quote_order_qty = 10
    # price = 0.0001
    timestamp = int(time.time() * 1000)  # Current timestamp in milliseconds

    # quoteOrderQty=10&recvWindow=5000&side=BUY&symbol=BTCUSDC&timestamp=1700594753821&type=MARKET
    # quoteOrderQty=10&recvWindow=5000&side=BUY&symbol=BTCUSDC&timestamp=1700595648335&type=MARKET&signature=e0c4d12f7f1b20ed35ddaee0d32de8b6eff5988fd72b014475ff4edb190b7e30


    # Create the signature
    data = f"quoteOrderQty={quote_order_qty}&recvWindow=5000&side={side}&symbol={symbol}&timestamp={timestamp}&type={type}"
    print(data)
    signature = hmac.new(config.SECRET_KEY.encode('utf-8'), data.encode('utf-8'), hashlib.sha256).hexdigest()
    print(signature)
    # Build the request URL
    url = f"{endpoint}?&quoteOrderQty={quote_order_qty}&recvWindow=5000&side={side}&symbol={symbol}&timestamp={timestamp}&type={type}&signature={signature}"
    print(url)
    
    headers = {
        "X-MEXC-APIKEY": config.API_KEY,
        "Content-Type": "application/json",  # Adjust as needed
    }

    # Make the API request
    try:
        response = requests.post(url, headers=headers)
        # Print the response
        print(response.json())

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")




    spot_client = spot.HTTP(api_key = config.API_KEY, api_secret = config.SECRET_KEY)


    # print(spot_client.account_information())
    # print(spot_client.exchange_info(
    #     symbols=["BTCUSDC"]))
    # print(spot_client.get_currency_info())
    # print(spot_client.order_book(symbol))
    # try:
    #     response = spot_client.new_order(
    #         symbol=symbol,
    #         side=side,
    #         order_type=type,
    #         quantity=quantity
    #     )

    #     print(response)

    # try:
    #     response = spot_client.new_order(
    #         symbol=symbol,
    #         side=side,
    #         order_type=type,
    #         quote_order_qty=quote_order_qty)
    #     # print(spot_client.get_currency_info())
    # except MexcAPIError as e:
    #     print(f"Error: {repr(e)}")
    #     print(f"Error Message: {e.message.decode('utf-8')}")

    # except Exception as e:
    #     print(f"Error: {e}")



