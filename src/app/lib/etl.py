import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
from .helpers import date_to_epoch, rule_90_day


NOW = datetime.now()


def _extract_supported_coins(cg):
    # Extract all supported coins id, name and symbol
    coins = cg.get_coins_list()
    return coins


def get_coin_data(cg, config):
    coin_name = config["coin_name"]
    currency = config["currency"]
    start_date = date_to_epoch(config["start_date"], True)
    end_date = date_to_epoch(
        rule_90_day(config["start_date"], config["end_date"]), False
    )

    # Extract all supported coins id, name and symbol
    coins = _extract_supported_coins(cg)

    # Get coin details
    for coin in coins:
        if coin["name"] == coin_name:
            coin_id = coin["id"]

    # Extract Coin Q1 2022 Jan to April due to 90 day limit
    coin_q1_2022 = cg.get_coin_market_chart_range_by_id(
        coin_id, currency, start_date, end_date
    )

    # Create dataframe to load to database
    df_coin_q1_2022 = pd.DataFrame()
    df_coin_q1_2022["date"] = [date[0] for date in coin_q1_2022["prices"]]
    df_coin_q1_2022["price"] = [data[1] for data in coin_q1_2022["prices"]]
    df_coin_q1_2022["extraction_date_utc"] = NOW

    print("Getting Q1 2022 details")
    print(df_coin_q1_2022.head())
    print(df_coin_q1_2022.info())

    return df_coin_q1_2022


def generate_moving_average(source_table, params, config):
    end_date = datetime.strptime(config["end_date"], "%Y%m%d")

    print(f"END DATE PARA MOVING AVERAGE: {end_date}")

    # Connection through SQLAlchemy needed to read from postgres db to df
    conn_string = (
        f"postgresql://{params['user']}@{params['host']}:5432/{params['database']}"
    )

    print(f"Connection string:  {conn_string}")

    db = create_engine(conn_string)
    conn_alchemy = db.connect()

    df = pd.read_sql_query(f"select date, price from {source_table}", con=conn_alchemy)

    print(df.info())
    print(df.head())

    print("=== Applying transformations ===")

    df["date"] = df["date"].apply(lambda x: datetime.fromtimestamp(x / 1000))
    df = df[df["date"] <= end_date]

    df["ma_5"] = df["price"].rolling(window=5).mean()

    print(df.info())
    print(df.head())

    return df
