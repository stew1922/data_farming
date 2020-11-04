"""
This file is to store functions to be used
accross notebooks

"""
import sys
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

# append folder path inside this folder
sys.path.insert(0,'data_farming/data/libs/libs/')

# Function to extract temp or prec

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
