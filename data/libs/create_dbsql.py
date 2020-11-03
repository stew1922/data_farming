# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
""" This notebook is designed to generate a postgreSQL
database with tables.

source: https://pythontic.com/database/postgresql/create%20database

"""
# Import Libraries
import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


# %%

# Load .env enviroment variables
load_dotenv()


# %%
# Connect to postgresql dbms
my_postgres_userid = os.getenv("POSTGRES_USER_ID")
my_postgres_password = os.getenv("POSTGRES_PASSWORD")

connect_command = f"user={my_postgres_userid} password={my_postgres_password}"
connection = psycopg2.connect(connect_command)
connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

# Obtain a DB cursor

cursor = connection.cursor()
name_database = "crop_prod_db"

sqlcreate_db = f"CREATE DATABASE {name_database}"

# Execute the command
cursor.execute(sqlcreate_db)


# %%
# Create tables 

dbsession2 = psycopg2.connect(database = name_database, user= my_postgres_userid, password = my_postgres_password)
dbcursor = dbsession2.cursor()
dbsession2.autocommit = True

query_tables_create = """
DROP TABLE IF EXISTS states CASCADE;
DROP TABLE IF EXISTS temperatures  CASCADE;
DROP TABLE IF EXISTS crop_name CASCADE;
DROP TABLE IF EXISTS crop_production_total CASCADE;

CREATE TABLE states (
	state_id SERIAL PRIMARY KEY
	, state_name CHAR(2)
);



CREATE TABLE temperatures (
	state_id INT NOT NULL,
	FOREIGN KEY (state_id) REFERENCES states(state_id)
	, year INT NOT NULL
	, jan FLOAT NOT NULL
	, feb FLOAT NOT NULL
	, mar FLOAT NOT NULL
	, apr FLOAT NOT NULL
	, may FLOAT NOT NULL
	, jun FLOAT NOT NULL
	, jul FLOAT NOT NULL
	, ago FLOAT NOT NULL
	, sep FLOAT NOT NULL
	, oct FLOAT NOT NULL
	, nov FLOAT NOT NULL
	, dec FLOAT NOT NULL
);



CREATE TABLE crop_name (
	crop_id SERIAL PRIMARY KEY
	, crop_name VARCHAR(255) 
);



CREATE TABLE crop_production_total (
	crop_id INT NOT NULL,
	FOREIGN KEY (crop_id) REFERENCES crop_name(crop_id),
	year DATE,
	march_1st BIGINT,
	jun_1st BIGINT,
	sep_1st BIGINT,
	dec_1st BIGINT
);


"""

dbcursor.execute(query_tables_create)
dbsession2.close()


# %%



