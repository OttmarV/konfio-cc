import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine

NOW = datetime.now()


def _extract_supported_coins(cg):
    # Extract all supported coins id, name and symbol
    coins = cg.get_coins_list()
    return coins


def get_coin_data(cg):
    # Extract all supported coins id, name and symbol
    coins = _extract_supported_coins(cg)

    # Get bitcoin details
    for coin in coins:
        if coin["id"] == "bitcoin":
            btc_id = coin["id"]

    # Extract bitcoin Q1 2022 Jan to April due to 90 day limit
    btc_q1_2022 = cg.get_coin_market_chart_range_by_id(
        btc_id, "usd", "1640995200", "1651363199"
    )

    # Create dataframe to load to database
    df_btc_q1_2022 = pd.DataFrame()
    df_btc_q1_2022["date"] = [date[0] for date in btc_q1_2022["prices"]]
    df_btc_q1_2022["price"] = [data[1] for data in btc_q1_2022["prices"]]
    df_btc_q1_2022["extraction_date_utc"] = NOW

    print("Getting q1 2022 details")
    print(df_btc_q1_2022.head())
    print(df_btc_q1_2022.info())

    return df_btc_q1_2022


def generate_moving_average(source_table, params):
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
    df["5_day_ma"] = df["price"].rolling(window=5).mean()

    print(df.info())
    print(df.head())

    return df
