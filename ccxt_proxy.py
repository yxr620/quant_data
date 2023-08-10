
import ccxt
import requests
import pandas as pd

from datetime import datetime

'''
before every test please make sure:(the proxy is correct)

export ALL_PROXY="http://127.0.0.1:7890" 
curl https://www.google.com
'''

'''
This is a basic test of proxy working
'''
# resp = requests.get('https://api.binance.com/api/v3/exchangeInfo', 
#                     proxies=dict(http='http://127.0.0.1:7890',
#                                  https='http://127.0.0.1:7890'))
# print(resp)

'''
binance exchange testing
'''
my_proxies = {
    'http': 'http://127.0.0.1:7890',
    'https': 'http://127.0.0.1:7890',
}
start = datetime(2020, 6, 2)
end = datetime(2020, 6, 3)
binance = ccxt.binance({
    'proxies': my_proxies,
})

ohlcv = binance.fetch_ohlcv('BTC/USDT', '1m', since=int(start.timestamp() * 1000), limit=100)

df = pd.DataFrame(ohlcv, columns=['time', 'open', 'high', 'low', 'close', 'volume'])
df['time'] = pd.to_datetime(df['time'], unit='ms')  
df.set_index('time', inplace=True)
print(df)

'''
other exchange testing, okx
'''
my_proxies = {
    'http': 'http://127.0.0.1:7890',
    'https': 'http://127.0.0.1:7890',
}
start = datetime(2020, 6, 2)
end = datetime(2020, 6, 3)
exchange = ccxt.okx({
    'proxies': my_proxies,
})
exchange.options['defaultType'] = 'spot'

ohlcv = exchange.fetch_ohlcv('BTC/USDT', '1m', since=int(start.timestamp() * 1000), limit=100)

df = pd.DataFrame(ohlcv, columns=['time', 'open', 'high', 'low', 'close', 'volume'])
df['time'] = pd.to_datetime(df['time'], unit='ms')  
df.set_index('time', inplace=True)
print(df)

