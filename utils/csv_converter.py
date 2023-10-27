import pandas as pd

# Read the Binance data CSV file
binance_data = pd.read_csv('1day.csv')

# Assuming the timestamps are in seconds, not milliseconds
binance_data['Open time'] = pd.to_datetime(binance_data['Open time'], unit='s').dt.strftime('%Y-%m-%d')


# Reorder the columns as per your desired order
new_order = ['Open time', 'Open', 'High', 'Low', 'Close', 'Volume']
binance_data = binance_data[new_order]

# Save the data to a new CSV file
binance_data.to_csv('formatted_data.csv', index=False)

