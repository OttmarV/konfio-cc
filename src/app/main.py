from lib import db_engine as dbe, etl, plot
import pycoingecko
import os

POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")


class Pipeline:
    def __init__(self, params, cg):
        self.params = params
        self.cg = cg

    def run(self):
        cur, conn = dbe.create_connection(self.params)
        dbe.drop_tables(cur, conn)
        dbe.create_tables(cur, conn)
        df = etl.get_coin_data(self.cg)
        dbe.write_df_to_table(cur, conn, df, "landing_bitcoin", self.params)
        df = etl.generate_moving_average("landing_bitcoin", params)
        dbe.write_df_to_table(cur, conn, df, "refined_bitcoin", self.params)
        plot.plot_moving_average(df)

        # dbe.set_staging(cur, conn, self.staging_file, columns_staging)
        # dbe.fill_from_staging_all(cur, conn)
        # dbe.drop_table(cur, conn, "staging")
        # count_tables = dbe.check_data(cur, conn, tables)

        # for k, v in count_tables.items():
        #     print("Table {0} has {1} records".format(k, v))
        # dbe.close_connection(cur, conn)


if __name__ == "__main__":
    params = {
        "host": POSTGRES_HOST,
        "database": POSTGRES_DB,
        "user": POSTGRES_USER,
        "password": POSTGRES_PASSWORD,
    }

    # Initialize CoinGecko API client
    cg = pycoingecko.CoinGeckoAPI()

    print(f"Database parameters: {params}")

    pipeline = Pipeline(params, cg)
    pipeline.run()
