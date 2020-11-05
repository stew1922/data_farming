# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
import calendar
import plotly.express as px
import hvplot.pandas
from sqlalchemy import create_engine
import seaborn as sns
import csv
from pathlib import Path
import matplotlib.pyplot as plt
from datetime import datetime

import os
import psycopg2
from dotenv import load_dotenv
#from .data.libs.utilit_func import my_sql_temp


# %%
# Load .env enviroment variables
load_dotenv()


# %%
# to organize corn total production

path_crop = Path ('../data/raw_data/tot_corn_prod_y_bystate.csv')
csv_data = pd.read_csv(path_crop)
df =pd.DataFrame(data=csv_data)


# %%
new_df = df[['Year','State','Commodity','Value']]
new_df.set_index('Year', inplace=True)
new_df.head()


# %%
# add the id_state number in a column
def set_value(row_number, assigned_value): # function extracted from:https://www.geeksforgeeks.org/python-creating-a-pandas-dataframe-column-based-on-a-given-condition/ 
    return assigned_value[row_number]

# create state_id dictionary
state_id_dict = {'NEBRASKA': 1,'IOWA': 2, 'ILLINOIS': 3}
crop_id_dict = {'CORN': 1,'SOYBEAN': 2, 'WHEAT': 3}

# add new column named state_id

new_df['state_id']=new_df['State'].apply(set_value, args=(state_id_dict,)) 
new_df['crop_id'] = new_df['Commodity'].apply(set_value, args=(crop_id_dict,))

new_df.rename(columns ={'State': 'state', 'Commodity': 'crop_name', 'Value': 'value' }, inplace=True)
new_df.sort_values('state_id', inplace=True)
final_df = new_df.rename_axis('year')
final_df.reset_index(inplace=True)
final_df['value'] = final_df['value'].str.replace(",","").astype(float)
final_df['year'] =pd.to_datetime(final_df['year'], format='%Y') 
final_df['year']=final_df['year'].dt.year


final_df.head()


# %%
# Load .env enviroment variables
load_dotenv()


# %%
my_postgres_userid = os.getenv("POSTGRES_USER_ID")
my_postgres_password = os.getenv("POSTGRES_PASSWORD")
dbsession2 = psycopg2.connect(database = "crop_prod_db", user= my_postgres_userid, password = my_postgres_password)
dbcursor = dbsession2.cursor()
dbsession2.autocommit = True


# %%
name_db_extract = 'crop_prod_db'

# Create a conexion with the state weather database

db_url = "postgresql://postgres:postgres@localhost:5432/"+ name_db_extract +""

engine = create_engine(db_url)
engine


# %%
cnx = engine.raw_connection()
final_df.to_sql(name='yearly_crop_production', con=engine, if_exists='append', index=False)


# %%



