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
    """This class represents the etl to follow.

    Attributes
    ----------
    params : (Dict[str, str])
        db settings to create a connection string
    config (Dict[str, str]): coin details for extraction
        coin name, currency, start date and end date
        family name of the person
    cg (pycoingecko.api.CoinGeckoAPI): coingecko api instance

    Methods
    -------
    info(additional=""):
        Prints the person's name and age.

    """

    def __init__(self, params, config, cg):
        """Constructs all the necessary attributes for the
        Pipeline object.

        Args:
            params (Dict[str, str]): db settings to create a
            connection string
            config (Dict[str, str]): coin details for extraction
        coin name, currency, start date and end date
            cg (pycoingecko.api.CoinGeckoAPI): coingecko api instance
        """
        self.params = params
        self.config = config
        self.cg = cg

    def run(self):
        """Executes que etl

        Returns
        -------
        None
        """
        # Create psycopg2 db connection
        cur, conn = dbe.create_connection(self.params)
        # Recreate needed tables from scratch
        dbe.drop_tables(cur, conn)
        dbe.create_tables(cur, conn)

        # Extract data for requested coin
        df = etl.get_coin_data(self.cg, self.config)

        # Write to landing table the result of the first extraction
        dbe.write_df_to_table(cur, df, "landing_coin", self.params)

        # Extract and generate moving average data
        df = etl.generate_moving_average("landing_coin", self.params, self.config)

        # Load transformed data to a refined table
        dbe.write_df_to_table(cur, df, "refined_coin", self.params)

        # Plot and save as image the moving average results
        plot.plot_moving_average(df, self.config)


if __name__ == "__main__":
    # Set parameters for db connection
    params = {
        "host": POSTGRES_HOST,
        "database": POSTGRES_DB,
        "user": POSTGRES_USER,
        "password": POSTGRES_PASSWORD,
    }

    # Obtain extraction details from execution parameters
    config = {
        "coin_name": sys.argv[1],
        "currency": sys.argv[2],
        "start_date": sys.argv[3],
        "end_date": sys.argv[4],
    }

    # Initialize CoinGecko API client
    cg = pycoingecko.CoinGeckoAPI()

    print(f"Database parameters: {params}")

    # Create and run the Pipeline object
    pipeline = Pipeline(params, config, cg)
    pipeline.run()
