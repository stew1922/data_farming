# The following defined functions are used to assist in the collection and data analysis of weather.
# Please use Python 3.8.5 and import library 'weather' to use the functions shown below.

# Import necessary libraries
import requests
import pandas as pd
import json
from pathlib import Path

def get_precipitation_and_average_temperature(station_id, start_date, end_date):
    '''Reads data from a designed and maintained API data source, Applied Climate Information 
    System (ACIS), by NOAA Regional Climate Centers (RCC), cleans the pulled data and returns 
    a dataframe of information.  Rows of missing values have been removed when specified by 'M'
    from the original dataset and precipitation data marked originally by 'T' are replaced with
    0.000001 to represent precipitation was captured on a given date, but no specific value was 
    provided in the source dataset.

    Args: 
        station_id (str): Weather station id (Example: 'KOMA')
        start_date (str): Starting date range formatted as yyyymmdd
        end_date (str): Ending date range formatted as yyyymmdd

    Returns: 
        A clean dataframe of information including column headings titled
        date, precipitation, and average temperature.  If arguments passed into function are 
        missing then return message to user.
    '''

    # Check that arguments were passed by user
    if station_id == '' or start_date == '' or end_date == '':
        return 'Missing station id, start date or end date.'
    # Arguments were passed successfully
    else:
        # API URL string
        rcc_url = f'http://data.rcc-acis.org/StnData?sid={station_id}&sdate={start_date}&edate={end_date}&meta=name&elems=pcpn,avgt&output=json'
        # Fetch current data
        response_data = requests.get(rcc_url)
        # Accept json format
        data = response_data.json()
        # Create dataframe
        weather_data =  pd.DataFrame(data['data'])

        # Create column headings and assign
        weather_data.columns = ['date', 'precipitation', 'average_temperature']

        # Drop rows with values of 'M' in precipitation column
        index_precep_rows = weather_data[weather_data['precipitation'] == 'M'].index
        weather_data.drop(index_precep_rows, inplace=True)

        # Drop rows with values of 'M' in average temperature column
        index_avgt_rows = weather_data[weather_data['average_temperature'] == 'M'].index
        weather_data.drop(index_avgt_rows, inplace=True)

        # Replace values of 'T' with 0.0001 to represent a value other than 0 or False
        # A measurement of precipitation was detected, but not provided
        weather_data['precipitation'] = weather_data['precipitation'].replace('T', 0.0001)

        # Change date values from object to datetime
        weather_data['date'] = pd.to_datetime(weather_data['date'])
        # Change precipitation values from object to type float
        weather_data['precipitation'] = weather_data['precipitation'].astype(float)
        # Change average_temperature values from object to type float
        weather_data['average_temperature'] = weather_data['average_temperature'].astype(float)

        # Set date index
        weather_data.set_index('date', inplace=True)

        # Return clean weather data
        return weather_data

def for_state(state_name, start_date, end_date, return_format):
    '''Calls multiple stations in a specified state based on a timeframe, retrieves 
    a daily precipitation and average temperature, if available, for each station, 
    averages the data of the three weather stations, drops the calculated values 
    returning null to now skew data, and combines values in a dataframe format.  

    Args:
        state_name (str): State postal abbreviation (Example: 'NE')
        start_date (str): Starting date range formatted as 'yyyymmdd'
        end_date (str): Ending date range formatted as 'yyyymmdd'
        return_format (str): Desired returned output is either 'csv' (comma separated
            value) or 'df' (dataframe)

    Returns:
        A clean dataframe of information including column headings titled
        date, precipitation, and average temperature if 'df' is specified or a 'csv'
        file is created in .  If arguments passed into function are 
        missing then return message to user.
    '''
    # Initialize variables
    # Dictionary of states and station codes.
    # Can create a connection to a sql db in the future to store this information for data growth
    state_station_codes = {
        'NE': ['KOMA', 'KCDR', 'KMCK'],
        'IA': ['KCID', 'KDSM', 'KALO'],
        'IL': ['KORD', 'KMDW', 'KSPI']
        }
    list_of_stations = []
    state_df = pd.DataFrame()

    # Check for valid arguments passed in by user
    if state_name == 'NE' or 'IA' or 'IL':
        # Get station ids for selected state
        list_of_stations = state_station_codes[state_name]

        # Get weather data for each station
        station_0 = get_precipitation_and_average_temperature(list_of_stations[0], start_date, end_date)
        station_1 = get_precipitation_and_average_temperature(list_of_stations[1], start_date, end_date)
        station_2 = get_precipitation_and_average_temperature(list_of_stations[2], start_date, end_date)
        
        # Add all station data into one dataframe
        state_df = station_0 + station_1 + station_2

        # Calculate average of combine data values
        state_df = state_df / 3

        # Round values in each column
        state_df = state_df.round({'precipitation': 4, 'average_temperature': 1})

        # Drop null values to now skew data
        state_df.dropna(inplace=True)

        # Return state dateframe
        if return_format == 'df':
            return state_df

        # Output to csv file
        elif return_format == 'csv':
            # Create output path and write data to csv
            csv_output_path = Path('./clean_data/state_weather_data_clean.csv')
            state_df.to_csv(csv_output_path)
        else:
            # Return message that return format not found
            return 'Return format specified not found.  Pass in df or csv as a string.'
    else: 
        # Return message that state not found
        return 'State not found.  Pass in NE, IA or IL as a string.'