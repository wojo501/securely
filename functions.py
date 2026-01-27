import polars as pl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
from datetime import datetime as dt

def print_traffic_for_days(df_agg, days=[21,22,23,24,25,26,27]):
    df_pd = df_agg.to_pandas()
    dummy_date = dt.date(dt.now())
    df_pd['plot_time'] = df_pd['time_bin'].apply(lambda t: dt.combine(dummy_date, t))

    # Filter to only show day 24

    date_str = '2020-12-'
    filter = []
    for day in days:
        filter.append(f"{date_str}{day:02d}")
    df_pd = df_pd[df_pd['day'].isin(filter)]

    g = sns.FacetGrid(
        df_pd, 
        col="day", 
        col_wrap=4,  
        height=4,   
        aspect=1.5   
    )

    g.map(sns.lineplot, "plot_time", "len", color="navy", linewidth=1.5)

    g.map(plt.axhline, y=340, color='red', linestyle='--', linewidth=2)

    g.set_titles(col_template="{col_name}", size=14)
    g.set_axis_labels("Time of Day", "Number of Requests")


    for ax in g.axes.flat:
        # Set the x-axis formatter and locator
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        ax.xaxis.set_major_locator(mdates.HourLocator(interval=4)) # Ticks every 4 hours
        
        # Add gridlines
        ax.grid(axis='both', linestyle='--', alpha=0.6)


    plt.suptitle('Requests per 5-Minute Interval (by Day)', fontsize=18, y=1.03)
    plt.tight_layout()