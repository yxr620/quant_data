import os
import pandas as pd


# Import Spot client and datetime module
from binance.spot import Spot  
from datetime import datetime, timedelta

# decide when to start download data
# return date from which starts to update, return the start time of the last entry
def get_last_time(pair, save_dir="/home/yxr/crypto_quant/data/realtime"):
    file_list = os.listdir(save_dir)
    if len(file_list) == 0: return datetime(2023, 1, 1)
    file_list.sort(reverse=True) # sort the list from present to old

    result = datetime.strptime(file_list[-1].split(".")[0], "%Y%m%d")
    for file in file_list:
        table = pd.read_csv(os.path.join(save_dir, file))
        sub_table = table[table["trading_pairs"] == pair]
        if sub_table.empty: continue

        last_timestamp = sub_table["start"].iloc[-1]
        result = datetime.fromtimestamp(last_timestamp / 1000)
        break

    return result

# download historical klines, the func will decide when to start download
# param:
#   pair: trading pair eg. BTCUSDT
#   client: Spot client
def download_pair(pair, client, save_dir="~/crypto_quant/data/realtime/"):

    # get the last updated datetime fmt
    start = get_last_time(pair, save_dir)
    end = datetime.fromtimestamp(client.time()['serverTime']/1000)

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
            table = pd.DataFrame(columns=['trading_pairs', 'start', 'end', 'open', 'high', 'low', 'close', 'volume', 'quote_volume', 'num_trades', 'taker_base_vol', 'taker_quote_vol', 'ignore'])

        # download data from current time to next_day
        next_day = current_day + timedelta(days=1)
        total_bars = []
        while current_time + timedelta(minutes=500) < next_day:
            bars = client.klines(
                pair,
                "1m",
                startTime=int(current_time.timestamp()*1000),
                endTime=int((current_time + timedelta(minutes=500)).timestamp()*1000)
            )
            total_bars.extend(bars)
            current_time += timedelta(minutes=500)
        # get the tail data
        bars = client.klines(
            pair,
            "1m",
            startTime=int(current_time.timestamp()*1000),
            endTime=int((next_day - timedelta(minutes=1)).timestamp()*1000)
        )

        # for bar in bars:
        #     timestamp = bar[0]
        #     open = bar[1] 
        #     high = bar[2]
        #     low = bar[3] 
        #     close = bar[4]
        #     volume = bar[5]
        #     end_stamp = bar[6]
        #     quote_volume = bar[7]
        #     num_trades = bar[8]
        #     buy_base_vol = bar[9]
        #     buy_quote_vol = bar[10]

        #     readable_start_timestamp = datetime.fromtimestamp(timestamp/1000).strftime('%Y-%m-%d %H:%M:%S')
        #     readable_end_timestamp = datetime.fromtimestamp(end_stamp/1000).strftime('%Y-%m-%d %H:%M:%S')

        #     print(f"{readable_start_timestamp}-{readable_end_timestamp} Open: {open}, High: {high}, Low: {low}, Close: {close}, Volume: {volume}")


        # save table to csv
        total_bars.extend(bars)
        total_bars = [[pair] + row for row in total_bars]
        new_table = pd.DataFrame(total_bars, columns=['trading_pairs', 'start', 'open', 'high', 'low', 'close', 'volume', 'end', 'quote_volume', 'num_trades', 'taker_base_vol', 'taker_quote_vol', 'ignore'])
        table = pd.concat([new_table, table], ignore_index=True)
        table = table.sort_values(by='trading_pairs').drop_duplicates()
        table.to_csv(save_dir + f"{current_day.strftime('%Y%m%d')}.csv", index=False)

        # increase day
        current_day += timedelta(days=1)
        current_time = current_day


    return bars

if __name__ == "__main__":
    # Set up proxy dictionary
    proxies = {'https': 'http://127.0.0.1:7890'}

    # Create Spot client instance using proxy
    client = Spot(proxies = proxies)


    # last_time = get_last_time(pair="ETHUSDT")
    # print(last_time)
    # last_time = get_last_time(pair="BTCUSDT")
    # print(last_time)
    # exit()

    download_pair("BTCUSDT", client, "./realtime/")

