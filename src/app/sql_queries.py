# DROP TABLES
landing_table_drop = "DROP TABLE IF EXISTS landing_bitcoin"
refined_table_drop = "DROP TABLE IF EXISTS refined_bitcoin"

# CREATE TABLES

landing_table_create = """
CREATE TABLE IF NOT EXISTS landing_bitcoin (
        date BIGINT,
        price DECIMAL,
        extraction_date_utc DATE
);
"""

refined_table_create = """
CREATE TABLE IF NOT EXISTS refined_bitcoin(
        date DATE,
        price DECIMAL,
        ma_5 DECIMAL,
        CONSTRAINT department_pkey PRIMARY KEY(date)
);
"""

## FILL  TABLES FROM STAGING

users_fill_from_staging = """
INSERT INTO USERS (first_name, last_name, email, phone1, phone2, zip, address, city, state, department_id, company_id)
select 
    s.first_name,
    s.last_name,
    s.email, 
    s.phone1, 
    s.phone2, 
    s.zip, 
    s.address, 
    s.city, 
    s.state, 
    d.id as department_id, 
    c.id as company_id
from staging s
LEFT JOIN companies c
ON s.company_name = c.company
LEFT JOIN departments d
ON s.department = d.department;
"""

companies_fill_from_staging = """
    insert into companies (company)
    select distinct company_name
    from staging;
"""

departments_fill_from_staging = """
    insert into departments (department)
    select distinct department
    from staging;
"""


create_table_queries = [landing_table_create, refined_table_create]
drop_table_queries = [landing_table_drop, refined_table_drop]
