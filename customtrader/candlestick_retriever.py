import websocket
import json
import ssl
import csv

class CandlestickWebSocketApp():
    def __init__(self, max_candles):
        self.latest_data = []
        self.max_candles = max_candles
        uri = "wss://wbs.mexc.com/ws"
        ws = websocket.WebSocketApp(uri,
                                    on_message=self.on_message,
                                    on_error=self.on_error,
                                    on_close=self.on_close)
        ws.on_open = self.on_open
        ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
        
    def on_message(self, ws, message):
        candlestick_data = json.loads(message)
        print(message)
        self.add_closed_candles(candlestick_data)

    def on_error(self, ws, error):
        print("WebSocket Error:", error)

    def on_close(self, ws, close_msg):
        print("WebSocket Closed:", close_msg)

    def on_open(self, ws):
        print("open")
        request_data = {
                "method": "SUBSCRIPTION",
                "params": [
                    "spot@public.kline.v3.api@BTCUSDT@Min1"
                ]
    }
        ws.send(json.dumps(request_data))

    #write candlestick data to a csv
    def write_to_csv(self, candlestick_data):
        with open('candlestick_data.csv', mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([
                        candlestick_data["d"]["k"]["t"],
                        candlestick_data["d"]["k"]["o"],
                        candlestick_data["d"]["k"]["h"],
                        candlestick_data["d"]["k"]["l"],
                        candlestick_data["d"]["k"]["c"],
                        candlestick_data["d"]["k"]["a"]
                    ])

    #check if candlestick contains the right data/format
    def is_valid_candlestick_data(self, data):
        if isinstance(data, dict):
            d = data.get('d')
            k = d.get('k') if d is not None else None

            return (
                d and k and
                'e' in d and d['e'] == 'spot@public.kline.v3.api' and
                'k' in d and isinstance(k, dict) and
                't' in k and 'o' in k and 'c' in k and 'h' in k and 'l' in k and 'v' in k and 'a' in k and 'T' in k and 'i' in k
            )
        return False

    #add closed candlesticks to the latest data list
    def add_closed_candles(self, data):
        if (self.latest_data):
            if(self.latest_data[-1]["d"]["k"]["t"] == data["d"]["k"]["t"]):
                  self.latest_data[-1] = data
            else:
                 if (len(self.latest_data) == self.max_candles):
                      self.latest_data.pop(0)
                 self.latest_data.append(data)
        elif (self.is_valid_candlestick_data(data)):
            self.latest_data.append(data)
         

