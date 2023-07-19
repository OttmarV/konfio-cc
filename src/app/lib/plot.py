from matplotlib import pyplot as plt
from datetime import datetime, timedelta
from typing import Dict, List
import pandas as pd


def plot_moving_average(df: pd.DataFrame, config: Dict[str, str]) -> None:
    """Plot fixed 5 moving average and price against dates in
    the same plot.

    Args:
        df (pd.DataFrame): data with dates, price and moving average
        config (Dict[str, str]): coin details for extraction
        coin name, currency, start date and end date
    """
    print("Plotting dataframe")

    # Day window or moving average
    tick_days = 5
    start_date = datetime.strptime(config["start_date"], "%Y%m%d")
    end_date = datetime.strptime(config["end_date"], "%Y%m%d")

    xticks = []
    date = start_date

    # Create a 5 day data point for date axis in the plot
    while date < end_date:
        xticks.append(date)
        date = date + timedelta(days=tick_days)

    # Set theme
    plt.style.use("seaborn-dark")

    # Set size
    plt.figure(figsize=(15, 10))

    # Set line plot properties
    plt.semilogy(df["date"], df["price"], color="grey")
    plt.semilogy(df["date"], df["ma_5"], color="purple")

    # Rotation of date labels
    plt.xticks(xticks, rotation=-25)

    # Set date title properties
    plt.xlabel("Q1 2022 Dates", fontsize=18).set_color("purple")

    # Set price and moving average title properties
    plt.ylabel("Price", fontsize=18, rotation=0).set_color("black")

    # Add grid y axis
    plt.grid(True, color="white", linewidth="0.5", linestyle="-.", axis="both")

    # Set gneral title properties
    plt.title(
        f"5 Day Rolling Average for {config['coin_name']} Q1 2022",
        fontsize=20,
        loc="right",
    ).set_color("Orange")

    # Save plot as image
    plt.savefig("./coin_moving_average.png")
