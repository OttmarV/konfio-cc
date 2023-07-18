from lib import db_engine as dbe, etl, plot
import sys
import pycoingecko
import os

# Define global variables from env variables
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")


class Pipeline:
    def __init__(self, params, config, cg):
        self.params = params
        self.config = config
        self.cg = cg

    def run(self):
        cur, conn = dbe.create_connection(self.params)
        dbe.drop_tables(cur, conn)
        dbe.create_tables(cur, conn)
        df = etl.get_coin_data(self.cg, self.config)
        dbe.write_df_to_table(cur, conn, df, "landing_coin", self.params)
        df = etl.generate_moving_average("landing_coin", self.params, self.config)
        dbe.write_df_to_table(cur, conn, df, "refined_coin", self.params)
        plot.plot_moving_average(df)


if __name__ == "__main__":
    params = {
        "host": POSTGRES_HOST,
        "database": POSTGRES_DB,
        "user": POSTGRES_USER,
        "password": POSTGRES_PASSWORD,
    }

    config = {
        "coin_name": sys.argv[1],
        "currency": sys.argv[2],
        "start_date": sys.argv[3],
        "end_date": sys.argv[4],
    }

    # Initialize CoinGecko API client
    cg = pycoingecko.CoinGeckoAPI()

    print(f"Database parameters: {params}")

    pipeline = Pipeline(params, config, cg)
    pipeline.run()
