# 使用binance_historical_data下载数据

第三方历史数据下载方式，直接在终端运行`getdata.py`即可。由于Binance会禁止某些地区的IP访问，因此需要设计代理，代理的设置见具体程序内容。

# 使用binance.spot下载数据

这种方式直接使用Binance官方接口spot下载交易数据。同样需要设置代理，不过binance的这个库可以比较方便的使用一个参数设置代理。使用`download_his.py`下载历史数据，历史数据会存放在`./realtime`目录下。程序中默认的代理为`127.0.0.1:7890`，这个代理需要在`download_his.py`和`utiils.py`中设置。

所有的量价信息根据日期进行存储，将每日的数据存在名称为`%Y-%m-%d.csv`的文件中,文件内容格式如下，一共13个feature。
trading_pairs, start, open, high, low, close, volume, end, quote_volume, num_trades, taker_base_vol, taker_quote_vol, ignore


对于数据有一些说明：

trading_pairs:交易对,如BTCUSDT

start:开始时间，格式为时间戳，精度为ms。并且开始时间一定是某一个分钟，后续不会有秒。如果需要将这个时间戳转换成datetime格式可以使用如下代码:
```python
datetime.datetime.fromtimestamp(start/1000)
```

# ccxt这个库

## BUG处理

首先ccxt这个库的proxy设置有问题，不能像文档中说明的那样设置代理，而是需要修改源码。或者用AI提供的方式设置代理。我已经修改代码
```python

# /home/yxr/anaconda3/envs/quant/lib/python3.8/site-packages/ccxt/base/exchange.py 
tmp_proxy = dict(http='http://127.0.0.1:7890',
                https='http://127.0.0.1:7890')
try:
    response = self.session.request(
        method,
        url,
        data=body,
        headers=request_headers,
        timeout=int(self.timeout / 1000),
        proxies=tmp_proxy,
        # proxies=proxies,
        verify=self.verify and self.validateServerSsl
    )

```
使用AI提供的代理方式设置代理为：
```python
my_proxies = {
    'http': 'http://127.0.0.1:7890',
    'https': 'http://127.0.0.1:7890',
}

binance = ccxt.binance({
    'proxies': my_proxies,
})
```
除了上述设置代理有bug，还有一个fetch_markets出现的错误。如果在fetch_markets时连续发出多个请求就会报错请求超时。需要将fetchMarkets这个list缩短为一个，只发出已请求能保证请求不超时。
```python
# /home/yxr/anaconda3/envs/quant/lib/python3.8/site-packages/ccxt/binance.py
for i in range(0, len(rawFetchMarkets)):
    type = rawFetchMarkets[i]
    if type == 'option' and sandboxMode:
        continue
    fetchMarkets.append(type)
fetchMarkets = fetchMarkets[:1]
```

除了这种笨蛋方式解决问题，还有一种比较奇怪的方式，就是在python发送请求的时候直接使用request.get发送请求，而不使用session.request
```python
# /home/yxr/anaconda3/envs/quant/lib/python3.8/site-packages/ccxt/base/exchange.py
if method == 'GET':
    response = requests.get(url, data=body, headers=request_headers, proxies=proxies, verify=self.verify and self.validateServerSsl)
else:
    response = self.session.request(
        method,
        url,
        data=body,
        headers=request_headers,
        timeout=int(self.timeout / 1000),
        proxies=proxies,
        verify=self.verify and self.validateServerSsl
    )
print(response)
```





