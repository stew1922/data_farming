from pathlib import Path
import pandas as pd

# Function to graph up Exponential Moving Averages for the monthly WASDE estimates
def wasde_monthly_ma():
    from pathlib import Path
    import pandas as pd
    
    # pull in the data from the consolidated wasde monthly reports
    clean_data_path = Path('../data/clean_data/monthly_wasde_reports.csv')

    # convert the date to datetimes and set as index
    clean_df = pd.read_csv(clean_data_path, parse_dates=True, infer_datetime_format=True)
    clean_df['date'] = pd.to_datetime(clean_df['date'])

    clean_df = clean_df.set_index('date')

    # create our base-line production plot
    prod_plot = (clean_df['production']/1000).hvplot(title='WASDE Annual Projection', ylabel='Production, Billion Bu', rot=45, xticks=9)
    prod_plot

    # monthly data, so 1 year = 12 * 1 and 5 year = 12 * 5
    window1 = 12 * 1
    window5 = 12 * 5

    # create the exponential moving average data
    ewm1 = pd.DataFrame((clean_df['production']/1000).ewm(span=window1).mean())
    ewm1.rename(columns={'production':'EMA 1-year'}, inplace=True)
    ewm5 = pd.DataFrame((clean_df['production']/1000).ewm(span=window5).mean())
    ewm5.rename(columns={'production':'EMA 5-year'}, inplace=True)

    # create the ema plots
    ewm1_plot = ewm1['EMA 1-year'].hvplot(title='WASDE Annual Projection', ylabel='Production, Billion Bu', line_width=2.5, color='darkorange')
    ewm5_plot = ewm5['EMA 5-year'].hvplot(title='WASDE Annual Projection', ylabel='Production, Billion Bu', color='magenta', line_width=2.5)

    # return the combined plot of moving averages
    return (prod_plot * ewm1_plot * ewm5_plot).opts(frame_height=300, legend_position='bottom_right', show_grid=True)

# Function to plot the beginning and ending inventory data and how inventory is growing/shrinking
def inventory():
    from pathlib import Path
    import pandas as pd
    
    # pull in the data from the consolidated wasde monthly reports
    clean_data_path = Path('../data/clean_data/monthly_wasde_reports.csv')

    # convert the date to datetimes and set as index
    clean_df = pd.read_csv(clean_data_path, parse_dates=True, infer_datetime_format=True)
    clean_df['date'] = pd.to_datetime(clean_df['date'])

    clean_df = clean_df.set_index('date')

    # create two dataframes for the beginning and ending stocks
    begin_df = pd.DataFrame(clean_df['beginning_stocks']/1000)
    begin_df.rename(columns={'beginning_stocks':'stocks'}, inplace=True)

    end_df = pd.DataFrame(clean_df['ending_stocks']/1000)
    end_df.rename(columns={'ending_stocks':'stocks'}, inplace=True)

    # subtract the beginning volumes from the ending volumes and put into a dataframe
    diff_df = -begin_df + end_df

    # create plots for each beginning, ending and difference in stocks and then combine them in one plot
    end_df_plot = end_df.rename(columns={'stocks':'Ending Stocks'})['Ending Stocks'].hvplot(ylabel='Production, Billion Bu', title='Change in Inventory Over Time', xticks=10, color='magenta')

    begin_df_plot = begin_df.rename(columns={'stocks':'Beginning Stocks'})['Beginning Stocks'].hvplot(ylabel='Production, Billion Bu', title='Change in Inventory Over Time', xticks=10)

    diff_df_plot = diff_df.rename(columns={'stocks':'Inventory Loss/Gain'})['Inventory Loss/Gain'].hvplot(kind='bar', xticks=10)

    return (diff_df_plot * end_df_plot * begin_df_plot).opts(show_legend=True, legend_position='top_left', frame_height=300, show_grid=True, xlabel="Months (start date, t0 = 07/2010)")