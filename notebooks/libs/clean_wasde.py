import os
import pandas as pd
from pathlib import Path
import datetime

def clean_wasde():
    import os
    import pandas as pd
    from pathlib import Path
    import datetime

    # use python to open the path of the directory which contains the WASDE reports
    # create a blank dataframe for the clean data to go into
    wasde_data = os.listdir(Path('../data/raw_data/wasde_data'))
    clean_data = pd.DataFrame(columns=['date', 'beginning_stocks', 'production', 'ending_stocks'])

    # loop through the excel files and extract the data into the clean_data df
    for data in wasde_data:
        wasde = Path(f'../data/raw_data/wasde_data/{data}')
        wasde_df = pd.read_excel(wasde, sheet_name='Page 12')

        if type(wasde_df.iloc[0][2]) == type('string'):
            # the data is in the older format (pre June 2012)
            wasde_df = pd.read_excel(wasde, sheet_name='Page 12', skiprow=[0], header=[1,31])
            if 'Unnamed' in wasde_df.columns[2][1]:
                # format 1 (pre September 2010)
                wasde_df = pd.read_excel(wasde, sheet_name='Page 12', skiprow=[0], header=[1,30])
                report_date = wasde_df.columns[2][0]
                report_real_date = datetime.datetime.isoformat(datetime.datetime.strptime(wasde_df.columns[2][0], '%B %Y'))

                clean_data = clean_data.append({
                    'date': report_real_date, 
                    'beginning_stocks': wasde_df[report_date].iloc[7, 4], 
                    'production': wasde_df[report_date].iloc[8, 4],
                    'ending_stocks': wasde_df[report_date].iloc[17, 4]},
                    ignore_index=True).sort_values('date', ascending=False)
            else:
                # format 2 (September 2010-May 2012)
                report_date = wasde_df.columns[2][0]
                report_real_date = datetime.datetime.isoformat(datetime.datetime.strptime(wasde_df.columns[2][0], '%B %Y'))

                clean_data = clean_data.append({
                    'date': report_real_date, 
                    'beginning_stocks': wasde_df[report_date].iloc[7, 4], 
                    'production': wasde_df[report_date].iloc[8, 4],
                    'ending_stocks': wasde_df[report_date].iloc[17, 4]},
                    ignore_index=True).sort_values('date', ascending=False)
        else:
            # the data is in the new format
            wasde_df = pd.read_excel(wasde, sheet_name='Page 12', header=[0, 29], skip_footer=2).tail(17).reset_index(drop=True)
            report_date = wasde_df.columns[0][0]
            report_real_date = datetime.datetime.isoformat(datetime.datetime.strptime(wasde_df.columns[0][0], '%B %Y'))

            clean_data = clean_data.append({
                'date': report_real_date, 
                'beginning_stocks': wasde_df[report_date].iloc[5,4], 
                'production': wasde_df[report_date].iloc[6, 4],
                'ending_stocks': wasde_df[report_date].iloc[15, 4]},
                ignore_index=True).sort_values('date', ascending=False)

    clean_data.set_index('date', inplace=True)
    clean_data.dropna(inplace=True)

    # write the df to a new .csv file in the clean_data directory
    df_writer = Path('../data/clean_data/monthly_wasde_reports.csv')
    clean_data.to_csv(df_writer)
    return "Data cleaned!"