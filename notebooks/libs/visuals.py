# This library is to store functions that call various visualizations for reusability

# Import necessary libraries
import hvplot.pandas
import matplotlib.pyplot as plt

def data_farm_line_chart(data_df, x_column_name, y_column_name, title, ylim_min, ylim_max):
    '''Accepts a dataframe of information and displays a line chart based on passed parameters'''
    
    # Plot the data here as a line chart
    fig_chart = plt.figure(figsize=(8, 5))
    plt.subplot()
    plt.plot(data_df[x_column_name], data_df[y_column_name])
    plt.title(title, size=18)
    plt.xlabel(x_column_name, size=14)
    plt.ylabel(y_column_name, size=14)


    plt.ylim(ylim_min, ylim_max)

    plt.close(fig_chart)
    
    return fig_chart

