import os
import json
import argparse
import requests
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pandas import date_range
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from pandas import Timestamp

fred_schedule = df_usr[df_usr['name'] == 'Fred Luddy']['schedule'].iloc[0]
fred_schedule = eval(fred_schedule)
howard_schedule = df_usr[df_usr['name'] == 'Howard Johnson']['schedule'].iloc[0]
howard_schedule = eval(howard_schedule)
charlie_schedule = df_usr[df_usr['name'] == 'Charlie Whitherspoon']['schedule'].iloc[0]
charlie_schedule = eval(charlie_schedule)

# Assuming df is already defined and has 'opened_at' and 'closed_at' columns converted to datetime
df['opened_at'] = pd.to_datetime(df['opened_at'])
df['closed_at'] = pd.to_datetime(df['closed_at'])

# Define the current date for the analysis, simulate up to the last 'opened_at' date
current_date = df['opened_at'].max()
# Create a range of dates from the start to the current date
date_range = pd.date_range(start=df['opened_at'].min(), end=current_date, freq='D')

# Fred's PTO schedule as list of tuples with start and end dates
pto_schedule = fred_schedule

# Plotting
fig, ax = plt.subplots(figsize=(10, 2))  # Adjust the figure size as needed

# Plot each leave period as a rectangle
for start, end in fred_schedule:
    ax.axvspan(start, end, color='red', alpha=0.5, label='PTO (Leave Period)')
for start, end in howard_schedule:
    ax.axvspan(start, end, color='blue', alpha=0.5, label='PTO (Leave Period)')
for start, end in charlie_schedule:
    ax.axvspan(start, end, color='green', alpha=0.5, label='PTO (Leave Period)')

# Set limits, labels, title and legend
ax.set_xlim([date_range.min(), date_range.max()])
ax.set_ylim(0, 1)  # Static Y limits as we are only plotting periods
ax.set_yticks([])  # Hide Y axis ticks
ax.set_xlabel('Date')
ax.set_title('Timeline of Fred Luddy\'s Leave Periods')
ax.legend(loc='upper right')

# Formatting the x-axis to make it more readable
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
