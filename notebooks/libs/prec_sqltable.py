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
def my_sql_temp (year, df):
    select_year = df.loc[df['year']==year]
    #print (year)
    # rename row months from numeric to alphabetic
    select_year['month'] = select_year['month'].replace([1],'jan')
    select_year['month'] = select_year['month'].replace([2],'feb')
    select_year['month'] = select_year['month'].replace([3],'mar')
    select_year['month'] = select_year['month'].replace([4],'apr')
    select_year['month'] = select_year['month'].replace([5],'may')
    select_year['month'] = select_year['month'].replace([6],'jun')
    select_year['month'] = select_year['month'].replace([7],'jul')
    select_year['month'] = select_year['month'].replace([8],'aug')
    select_year['month'] = select_year['month'].replace([9],'sep')
    select_year['month'] = select_year['month'].replace([10],'oct')
    select_year['month'] = select_year['month'].replace([11],'nov')
    select_year['month'] = select_year['month'].replace([12],'dec')
    select_year.rename(columns={'average_temperature': f'{year}'}, inplace=True)
    #new_data_year = select_year.drop(columns='year')
    select_year.drop(columns='year',inplace = True)
    #print (new_data_year)
    #print (select_year)
    transposed_df = select_year.transpose()
    transposed_df.reset_index(inplace=True)
    transposed_df['index'] = transposed_df['index'].replace(['month'],'year')
    transposed_df.columns = transposed_df.iloc[0]
    transposed_df.drop(index=0, inplace=True)
    new_df = pd.DataFrame(transposed_df)
    return (new_df)


# %%
# Upload temperature for each state
"""
1) get the clean csv data
"""
list_to_extract = ['NE','IA','IL']
year_ini = 2001
year_end = 2020
name_database = "crop_prod_db"

for int in list_to_extract:
    state_ini = int

    path_temp = Path (f'../../data/clean_data/{state_ini}_weather_data_clean.csv')
    csv_data = pd.read_csv(path_temp)
    df =pd.DataFrame(data=csv_data)
    type(df['date'])
    df.dtypes
    df['date'] = pd.to_datetime(df['date'])
    df.dtypes # this is to identify the type of variable that column "date" is
    
    df['day'] = df['date'].dt.day
    df['month'] =df['date'].dt.month
    df['year'] = df['date'].dt.year
    monthly_temp_precp = df.groupby(['year','month']).mean().round(decimals = 5)
    monthly_temp_precp.drop(columns='day', inplace = True)
    monthly_temp = monthly_temp_precp.drop(columns='average_temperature')
    monthly_temp.reset_index(inplace=True)
    monthly_temp
    
    df = monthly_temp
    state_dt_to_table = state_ini


    my_postgres_userid = os.getenv("POSTGRES_USER_ID")
    my_postgres_password = os.getenv("POSTGRES_PASSWORD")
    dbsession2 = psycopg2.connect(database = name_database, user= my_postgres_userid, password = my_postgres_password)
    dbcursor = dbsession2.cursor()
    dbsession2.autocommit = True
    
    for int in range (year_ini,year_end):
        my_df_a = my_sql_temp (int,df)
        pd.DataFrame(my_df_a)
        my_df = my_df_a.set_index('year')
        type(my_df)
        jan_temp = my_df.iloc[0]['jan']
        feb_temp = my_df.iloc[0]['feb']
        mar_temp = my_df.iloc[0]['mar']
        apr_temp = my_df.iloc[0]['apr']
        may_temp = my_df.iloc[0]['may']
        jun_temp = my_df.iloc[0]['jun']
        jul_temp = my_df.iloc[0]['jul']
        aug_temp = my_df.iloc[0]['aug']
        sep_temp = my_df.iloc[0]['sep']
        oct_temp = my_df.iloc[0]['oct']
        nov_temp = my_df.iloc[0]['nov']
        dec_temp = my_df.iloc[0]['dec']
        state_temp_to_upload = state_dt_to_table 

        if state_temp_to_upload == 'NE' :
            state_id = 1
        elif state_temp_to_upload == 'IA' :
            state_id = 2
        elif state_temp_to_upload == 'IL':
            state_id = 3
        else :
            state_id = 100
        
        insert_query = """

        INSERT INTO precipitations
        (state_id, year, jan, feb,mar,apr,may,jun,jul,ago, sep, oct, nov,dec )
        VALUES
        (""" +str(state_id)+""",""" + str(int)+""", """ +str(jan_temp)+""","""+str(feb_temp)+""",""" +str(mar_temp)+""","""+str(apr_temp)+""","""+str(may_temp)+""","""             +str      (jun_temp)+""","""+str(jul_temp)+""","""+str(aug_temp)+""","""+str(sep_temp)+""","""+str(oct_temp)+""","""+str(nov_temp)+""","""+str(dec_temp)+""");
        """
    
        dbcursor.execute(insert_query)



# %%

dbsession2.close()


