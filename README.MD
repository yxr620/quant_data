## 使用binance_historical_data下载数据

第三方历史数据下载方式，直接在终端运行`getdata.py`即可。由于Binance会禁止某些地区的IP访问，因此需要设计代理，代理的设置见具体程序内容。

## 使用binance.spot下载数据

这种方式直接使用Binance官方接口spot下载交易数据。同样需要设置代理，不过binance的这个库可以比较方便的使用一个参数设置代理。使用`download_his.py`下载历史数据，历史数据会存放在`./realtime`目录下。程序中默认的代理为`127.0.0.1:7890`，这个代理需要在`download_his.py`和`utiils.py`中设置。

所有的量价信息根据日期进行存储，将每日的数据存在名称为`%Y-%m-%d.csv`的文件中,文件内容格式如下，一共13个feature。
trading_pairs, start, open, high, low, close, volume, end, quote_volume, num_trades, taker_base_vol, taker_quote_vol, ignore


对于数据有一些说明：

trading_pairs:交易对,如BTCUSDT

start:开始时间，格式为时间戳，精度为ms。并且开始时间一定是某一个分钟，后续不会有秒。如果需要将这个时间戳转换成datetime格式可以使用如下代码:
```python
datetime.datetime.fromtimestamp(start/1000)
```






