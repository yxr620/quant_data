import os
import pandas as pd
from datetime import datetime

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

check_data("./realtime/")
