# DROP TABLES
landing_table_drop = "DROP TABLE IF EXISTS landing_coin"
refined_table_drop = "DROP TABLE IF EXISTS refined_coin"

# CREATE TABLES

landing_table_create = """
CREATE TABLE IF NOT EXISTS landing_coin (
        date BIGINT,
        price DECIMAL,
        extraction_date_utc DATE
);
"""

refined_table_create = """
CREATE TABLE IF NOT EXISTS refined_coin(
        date DATE,
        price DECIMAL,
        ma_5 DECIMAL,
        CONSTRAINT department_pkey PRIMARY KEY(date)
);
"""

create_table_queries = [landing_table_create, refined_table_create]
drop_table_queries = [landing_table_drop, refined_table_drop]
