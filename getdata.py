'''
use this code to download history data from binance binance_historical_data

'''

import urllib.request
import datetime

# Set up proxy
proxy_url = 'http://127.0.0.1:7890'
opener = urllib.request.build_opener(urllib.request.ProxyHandler({'http': proxy_url, 'https': proxy_url}))
urllib.request.install_opener(opener)

from binance_historical_data import BinanceDataDumper

data_dumper = BinanceDataDumper(
    path_dir_where_to_dump="./data",
    asset_class="spot",  # spot, um, cm
    data_type="klines",  # aggTrades, klines, trades
    data_frequency="1m",
)

data_dumper.dump_data()


# * Open time" - Timestamp
# * Open"
# * High"
# * Low"
# * Close"
# * Volume"
# * Close time" - Timestamp
# * Quote asset volume"
# * Number of trades"
# * Taker buy base asset volume"
# * Taker buy quote asset volume"
# * Ignore"