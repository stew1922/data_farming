import pandas as pd
import numpy as np
import json
import requests


def pull_usda_data(usda_api_key, commodity, statistic, agg_level, year):

    #assign usda api url and establish which parameter will be fed as variables
    usda_url = f'http://quickstats.nass.usda.gov/api/api_GET/?key={usda_api_key}&source_desc=SURVEY&commodity_desc={commodity}&statisticcat_desc={statistic}&agg_level_desc={agg_level}&year_GE={year}&format=JSON'

    #get usda data via api and return as json
    usda_data = requests.get(usda_url).json()

    #put dictionary from returned json data into df
    usda_df = pd.DataFrame(usda_data['data'])

    #assign variable as list of data columns to use to slice usda_df
    data_columns = ['commodity_desc', 'util_practice_desc', 'state_alpha', 'statisticcat_desc', 'unit_desc', 'freq_desc', 'year', 'reference_period_desc', 'Value']  

    #slice usda_df with assigned columns prior to cleaning data
    usda_df_clean = usda_df[data_columns]

    #replace column names
    new_columns = ['commodity', 'sub_commodity', 'location', 'stat', 'unit', 'frequency', 'year', 'period', 'value']
    
    column_dict = dict(zip(data_columns, new_columns))
    usda_df_clean = usda_df_clean.rename(columns = column_dict)

    #clean columns so data is easy to use as time series
    usda_df_clean['value'] = usda_df_clean['value'].apply(lambda x: x.replace(',', ''))
    usda_df_clean['value'] = pd.to_numeric(usda_df_clean['value'], errors = 'coerce')
    usda_df_clean = usda_df_clean.fillna(np.nan)
    usda_df_clean['value'] = usda_df_clean['value'].astype('Int64')
    usda_df_clean['location'] = usda_df_clean['location'].replace('OT', 'other_states')
    usda_df_clean = usda_df_clean = usda_df_clean.sort_values(by = ['commodity', 'sub_commodity', 'location', 'stat', 'year'])
    usda_df_clean = usda_df_clean.loc[usda_df_clean['year'] >= 2000, :]
    usda_df_clean = usda_df_clean.reset_index(drop = True)

    return usda_df_clean