import pandas as pd
import pycoingecko
from datetime import datetime
from typing import Dict, List

from sqlalchemy import create_engine
from .helpers import date_to_epoch, rule_90_day


# Define global variables
NOW = datetime.now()


def _extract_supported_coins(cg: pycoingecko.api.CoinGeckoAPI) -> List[str]:
    """Extraction of supported coins to get all available coins

    Args:
        cg (pycoingecko.api.CoinGeckoAPI): coingecko api instance

    Returns:
        List[str]: coins id, name and symbol for all coins available
    """
    # Extract all supported coins id, name and symbol
    coins = cg.get_coins_list()
    return coins


def get_coin_data(
    cg: pycoingecko.api.CoinGeckoAPI, config: Dict[str, str]
) -> pd.DataFrame:
    """Extract price data for the requested coin using
    pycoingecko methods.

    90 day rule: Due to API coingecko limitations, if the start
    date and end date range is more than 90 days, data granularity
    will be daily, meaning one data point per day. To make life
    easier, we always will extract a minimum of 90 days of data
    regardless the input end_date. However, refined table with
    the moving average will just contain data until the input
     end_date

    Args:
        cg (pycoingecko.api.CoinGeckoAPI): coingecko api instance
        config (Dict[str, str]): coin details for extraction
        coin name, currency, start date and end date

    Returns:
        pd.DataFrame: data extracted with columns date, price and
        extraction_date_utc
    """
    coin_name = config["coin_name"]
    currency = config["currency"]
    start_date = date_to_epoch(config["start_date"], True)

    # Evaluating 90 day rule
    end_date = date_to_epoch(
        rule_90_day(config["start_date"], config["end_date"]), False
    )

    # Extract all supported coins id, name and symbol
    coins = _extract_supported_coins(cg)

    # Get coin details
    for coin in coins:
        if coin["name"] == coin_name:
            coin_id = coin["id"]

    # Extract Coin data by date range
    coin_q1_2022 = cg.get_coin_market_chart_range_by_id(
        coin_id, currency, start_date, end_date
    )

    # Create dataframe with coin prices to load to database
    # Add extraction_date_utc to keep track of latest extraction in UTC
    df = pd.DataFrame()
    df["date"] = [date[0] for date in coin_q1_2022["prices"]]
    df["price"] = [data[1] for data in coin_q1_2022["prices"]]
    df["extraction_date_utc"] = NOW

    print("Getting df Q1 2022 details")
    print(df.info())

    return df


def generate_moving_average(
    source_table: str, params: Dict[str, str], config: Dict[str, str]
) -> pd.DataFrame:
    """Create a fixed 5 day moving average.
    Moving average: statistic that captures the average change
    in a data series over time.


    Args:
        source_table (str): Data before processing
        params (Dict[str, str]): db settings to create a
        connection string
        config (Dict[str, str]): coin details for extraction
        coin name, currency, start date and end date

    Returns:
        pd.DataFrame: data with date, price and 5 day moving
        average
    """
    end_date = datetime.strptime(config["end_date"], "%Y%m%d")

    print(f"End date for moving average calculation: {end_date}")

    # Connection through SQLAlchemy needed to read from postgres db to df
    conn_string = (
        f"postgresql://{params['user']}@{params['host']}:5432/{params['database']}"
    )

    print(f"Connection string: {conn_string}")

    # Create connection through SQLAlchemy
    db = create_engine(conn_string)
    conn_alchemy = db.connect()

    # Read data from source table
    df = pd.read_sql_query(f"select date, price from {source_table}", con=conn_alchemy)

    print(df.info())

    print("=== Applying transformations ===")

    print("=== Transformation: Epoch to calendar date ===")
    df["date"] = df["date"].apply(lambda x: datetime.fromtimestamp(x / 1000))
    df = df[df["date"] <= end_date]

    print("=== Transformation: Calculating 5 day moving average ===")
    df["ma_5"] = df["price"].rolling(window=5).mean()

    print(df.info())
    print(df.head())

    return df
