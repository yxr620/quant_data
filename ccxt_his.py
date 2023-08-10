import ccxt
import requests
import pandas as pd
import os
import pandas as pd


from datetime import datetime
from datetime import datetime, timedelta


# decide when to start download data
# return date from which starts to update, return the start time of the last entry
def get_last_time(pair, save_dir="/home/yxr/crypto_quant/data/realtime"):
    file_list = os.listdir(save_dir)
    if len(file_list) == 0: return datetime(2023, 1, 1)
    file_list.sort(reverse=True) # sort the list from present to old

    result = None
    for file in file_list:
        table = pd.read_csv(os.path.join(save_dir, file))
        sub_table = table[table["trading_pairs"] == pair]
        if sub_table.empty: continue

        last_timestamp = sub_table["start"].iloc[-1]
        result = datetime.fromtimestamp(last_timestamp / 1000)
        break

    if result == None:
        return datetime(2023, 1, 1)
    return result


# download historical klines, the func will decide when to start download
# param:
#   pair: trading pair eg. BTCUSDT
#   client: Spot client
def download_pair(pair, client, save_dir="~/crypto_quant/data/realtime/"):

    # get the last updated datetime fmt
    start = get_last_time(pair, save_dir)
    end = datetime.fromtimestamp(client.fetch_time()/1000)

    # start = (start + timedelta(minutes=1))
    current_day = datetime(start.year, start.month, start.day)
    end_day = datetime(end.year, end.month, end.day)
    current_time = start
    print(f"start {start}")
    print(f"current_day {current_day}")
    print(f"end {end}")
    print(f"end_day {end_day}")
    print(f"current_time {current_time}")

    while current_day <= end_day:
        print(current_day)
        # if current exist table, load table
        if os.path.exists(save_dir + f"{current_day.strftime('%Y%m%d')}.csv"):
            table = pd.read_csv(save_dir + f"{current_day.strftime('%Y%m%d')}.csv")
        else:
            table = pd.DataFrame(columns=['trading_pairs', 'start', 'open', 'high', 'low', 'close', 'volume'])

        # download data from current time to next_day
        next_day = current_day + timedelta(days=1)
        total_bars = []
        limit = 100
        while current_time + timedelta(minutes=limit) < next_day:
            bars = client.fetch_ohlcv(
                pair,
                "1m",
                since=int(current_time.timestamp()*1000),
                limit=limit
            )
            total_bars.extend(bars)
            current_time += timedelta(minutes=limit)
        # get the tail data

        bars = client.fetch_ohlcv(
            pair,
            "1m",
            since=int(current_time.timestamp()*1000),
            limit=limit
        )

        # save table to csv
        total_bars.extend(bars)
        total_bars = [[pair] + row for row in total_bars]
        new_table = pd.DataFrame(total_bars, columns=['trading_pairs', 'start', 'open', 'high', 'low', 'close', 'volume'])
        table = pd.concat([new_table, table], ignore_index=True)
        table = table.sort_values(by=['trading_pairs', 'start']).drop_duplicates(subset=['trading_pairs', 'start'])
        table = table[table['start'] < next_day.timestamp() * 1000]

        table.to_csv(save_dir + f"{current_day.strftime('%Y%m%d')}.csv", index=False)

        # increase day
        current_day += timedelta(days=1)
        current_time = current_day

    return bars

if __name__ == "__main__":
    my_proxies = {
        'http': 'http://127.0.0.1:7890',
        'https': 'http://127.0.0.1:7890',
    }
    exchange = ccxt.okx({
        'proxies': my_proxies,
    })

    dir = "./okx/"
    download_pair("BTC/USDT", exchange, dir)
