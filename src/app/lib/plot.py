from matplotlib import pyplot as plt
from datetime import datetime, timedelta
from typing import Dict, List
import pandas as pd


def plot_moving_average(df: pd.DataFrame, config: Dict[str, str]) -> None:
    print("Plotting dataframe")

    tick_days = 5
    start_date = datetime.strptime(config["start_date"], "%Y%m%d")
    end_date = datetime.strptime(config["end_date"], "%Y%m%d")

    xticks = []
    date = start_date

    while date < end_date:
        xticks.append(date)
        date = date + timedelta(days=tick_days)

    plt.style.use("seaborn-dark")

    plt.figure(figsize=(15, 10))
    plt.semilogy(df["date"], df["price"], color="grey")
    plt.semilogy(df["date"], df["ma_5"], color="purple")
    plt.xticks(xticks, rotation=-25)
    plt.xlabel("Q1 2022 Dates", fontsize=18).set_color("purple")
    plt.ylabel("Price", fontsize=18, rotation=0).set_color("black")
    plt.grid(True, color="white", linewidth="0.5", linestyle="-.", axis="both")
    plt.title(
        f"5 Day Rolling Average for {config['coin_name']} Q1 2022",
        fontsize=20,
        loc="right",
    ).set_color("Orange")
    plt.savefig("./q1_2022.png")
