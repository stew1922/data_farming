# The following defined functions are used to assist in the collection and data analysis of weather.
# Please use Python 3.8.5 and import library 'weather' to use the functions shown below.

# Import necessary libraries
import requests
import pandas as pd
import json

def get_precipitation_and_average_temperature(station_id, start_date, end_date):
    '''Reads data from a designed and maintained API data source, Applied Climate Information 
    System (ACIS), by NOAA Regional Climate Centers (RCC), cleans the pulled data and returns 
    a dataframe of information.  Rows of missing values have been removed when specified by 'M'
    from the original dataset and precipitation data marked originally by 'T' are replaced with
    0.000000001 to represent precipitation was captured on a given date, but no specific value was 
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

        # Drop rows with values of 'M'
        index_rows = weather_data[weather_data.average_temperature == 'M'].index
        clean_weather_data = weather_data.drop(index_rows)
        # Replace values of 'T' with 0.000000001 to represent a value other than 0 or False
        # A measurement of precipitation was detected, but not provided
        clean_weather_data['precipitation'] = clean_weather_data['precipitation'].replace('T', 0.000000001)

        # Change date values from object to datetime
        clean_weather_data['date'] = pd.to_datetime(clean_weather_data['date'])
        # Change precipitation values from object to type float
        clean_weather_data['precipitation'] = clean_weather_data['precipitation'].astype(float)
        # Change average_temperature values from object to type float
        clean_weather_data['average_temperature'] = clean_weather_data['average_temperature'].astype(float)

        # Set date index
        clean_weather_data.set_index('date', inplace=True)

        # Return clean weather data
        return clean_weather_data
