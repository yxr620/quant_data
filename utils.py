import os
import pandas as pd
import urllib.request


from datetime import datetime, timedelta
from binance_historical_data import BinanceDataDumper

def visualize_row(row):
    """Visualize a DataFrame row."""
    trading_pairs = row["trading_pairs"]
    start = datetime.fromtimestamp(row["start"] / 1000)
    open = row["open"]
    high = row["high"]
    low = row["low"]
    close = row["close"]
    volume = row["volume"]
    end = datetime.fromtimestamp(row["end"] / 1000)
    quote_volume = row["quote_volume"]
    num_trades = row["num_trades"]
    taker_base_vol = row["taker_base_vol"]
    taker_quote_vol = row["taker_quote_vol"]
    print(f"""
Trading pair: {trading_pairs}
Start: {start}, {row["end"]}
Open: {open}  
High: {high}
Low: {low}   
Close: {close}
Volume: {volume}
End: {end}, {row["end"]}
Quote Volume: {quote_volume}  
Number of trades: {num_trades}
Taker base volume: {taker_base_vol}
Taker quote volume: {taker_quote_vol}
    """)

# check trading pair integrity from two perspective:
# 1. judge line correctness: total_line = 1440
# 2. judge date correctness: check start time is consistent with file name date
def check_data(dir):
    file_list = os.listdir(dir)
    file_list.sort()
    for file in file_list[:-1]:
        date = datetime.strptime(file.split(".")[0], "%Y%m%d")
        table = pd.read_csv(os.path.join(dir, file))
        correct_line_num = 24 * 60

        # get of trading_pairs set
        pair_set = set(table["trading_pairs"])
        group = table.groupby("trading_pairs")

        # judge line num
        for pair in pair_set:
            sub_table = group.get_group(pair)
            if len(sub_table) != correct_line_num:
                print(f"Error: {file} has incorrect line num for {pair}, get {len(sub_table)} lines")
                visualize_row(sub_table.iloc[0])
                
        
        # judge date time correctness
        for index, row in table.iterrows():
            if date != datetime.fromtimestamp(row["start"] / 1000).replace(hour=0, minute=0, second=0):
                print(f"Error: {file} has incorrect datetime for {pair}")
                visualize_row(row)

# fix data missing in case of exchange failure
def fix_missing_data(src_dir):
    file_list = os.listdir(src_dir)
    file_list.sort()

    for file in file_list[:-1]:
        date = datetime.strptime(file.split(".")[0], "%Y%m%d")
        table = pd.read_csv(os.path.join(src_dir, file))
        correct_line_num = 24 * 60

        # get of trading_pairs set
        pair_set = set(table["trading_pairs"])
        group = table.groupby("trading_pairs")

        # check ever pair has correct line num
        for pair in pair_set:
            sub_table = group.get_group(pair)
            if len(sub_table) != correct_line_num:
                print(f"Error: {file} has incorrect line num for {pair}, get {len(sub_table)} lines")
                visualize_row(sub_table.iloc[-1])

                # find missing time, the missed time is in list: missing_time
                iter_time = datetime.fromtimestamp(sub_table["start"].iloc[-1] / 1000)
                end_date = datetime.fromtimestamp(sub_table["start"].iloc[-1] / 1000).replace(hour=0, minute=0, second=0) + timedelta(days=1)
                missing_time = []
                while iter_time < end_date:
                    if iter_time.timestamp() * 1000 not in sub_table["start"]:
                        missing_time.append(iter_time)
                    iter_time += timedelta(minutes=1)
        


                # fill missing data with previous value
                # TODO
                for iter_time in missing_time:
                    # fill data with 0 or previous data???
                    pass
                    
        # save updated

# get the first apearing time of a trading pair
def first_time(pair):
    proxy_url = 'http://127.0.0.1:7890'
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({'http': proxy_url, 'https': proxy_url}))
    urllib.request.install_opener(opener)

    data_dumper = BinanceDataDumper(
        path_dir_where_to_dump="./his_data",
        asset_class="spot",  # spot, um, cm
        data_type="klines",  # aggTrades, klines, trades
        data_frequency="1m",
    )
    result = data_dumper.get_min_start_date_for_ticker(pair)

    return datetime(result.year, result.month, result.day)


# check_data("./realtime/")


