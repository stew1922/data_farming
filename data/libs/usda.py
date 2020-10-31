import requests
import pandas as pd
import json


def pull_usda_data(usda_api_key, commodity, statistic, state, year):

    #assign usda api url and establish which parameter will be fed as variables
    usda_url = f'http://quickstats.nass.usda.gov/api/api_GET/?key={usda_api_key}&source_desc=SURVEY&commodity_desc={commodity}&statisticcat_desc={statistic}&agg_level_desc=STATE&state_alpha={state}&year_GE={year}&format=JSON'

    #get usda data via api and return as json
    usda_data = requests.get(usda_url).json()

    #put dictionary from returned json data into df
    usda_df = pd.DataFrame(usda_data['data'])

    #assign variable as list of data columns to use to slice usda_df
    data_columns = ['commodity_desc', 'state_alpha', 'statisticcat_desc', 'util_practice_desc', 'unit_desc', 'state_alpha', 'freq_desc', 'year', 'reference_period_desc', 'Value']  
    
    #slice usda_df with assigned columns prior to cleaning data
    usda_df_clean = usda_df[data_columns]

    #clean Value column so datatype is numeric
    usda_df_clean['Value'] = usda_df_clean['Value'].apply(lambda x: x.replace(',', ''))
    usda_df_clean['Value'] = usda_df_clean['Value'].apply(lambda x: int(x))

    return usda_df_clean