import psycopg2
import pandas as pd

from sqlalchemy import create_engine
from sql_queries import create_table_queries, drop_table_queries


def create_connection(params: dict[str, str]):
    """
     create a new connection with the postgreSQL
     database and return the cur and conn object
    :param params: connection string
    """
    conn = None

    try:
        print("Connecting to the PostgreSQL database")
        conn = psycopg2.connect(**params)
        conn.set_session(autocommit=True)
        cur = conn.cursor()

        print("PostgreSQL database version:")
        cur.execute("SELECT version()")

        db_version = cur.fetchone()
        print(db_version)
        return cur, conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def close_connection(cur: psycopg2.extensions.cursor, conn):
    """
     close the connection with the postgreSQL database
    :param cur: cursor
    :param conn: connection object
    """
    try:
        cur.close()
        if conn is not None:
            conn.close()
            print("Database connection closed")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def drop_tables(cur: psycopg2.extensions.cursor, conn):
    """
     drop all the tables in the example
    :param cur: cursor
    :param conn: connection object
    """
    print("Dropping tables")
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()
    print("Tables dropped")


def create_tables(cur: psycopg2.extensions.cursor, conn):
    """
     create all the tables in the example
    :param cur: cursor
    :param conn: connection object
    """
    print("Creating tables")
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()
    print("Tables created")


def check_data(cur: psycopg2.extensions.cursor, conn, tables: list[str]):
    """
     Check count of records in tables
    :param cur: cursor
    :param conn: connection object
    :param tables: tables to check
    """

    count_values = {}

    for table in tables:
        query_count = "SELECT COUNT(*) FROM {0}".format(table)

        try:
            cur = conn.cursor()
            cur.execute(query_count)
            count_values[table] = cur.fetchone()[0]
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error: %s" % error)
            raise

    return count_values


def write_df_to_table(
    cur: psycopg2.extensions.cursor, df: pd.DataFrame, table: str, params: dict
) -> None:
    # Connection through SQLAlchemy needed to write df to postgres db
    conn_string = (
        f"postgresql://{params['user']}@{params['host']}:5432/{params['database']}"
    )

    print(f"Connection string:  {conn_string}")

    db = create_engine(conn_string)
    conn_alchemy = db.connect()

    print(f"Writing to table {table}")

    df.to_sql(table, con=conn_alchemy, if_exists="replace", index=False)

    print(f"Done writing to table {table}")

    sql = f"SELECT count(*) FROM {table}"

    cur.execute(sql)

    print(cur.fetchall())
