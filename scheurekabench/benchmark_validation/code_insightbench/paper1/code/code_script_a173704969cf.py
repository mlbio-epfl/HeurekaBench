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
import seaborn as sns

# Assuming df is your DataFrame and it has columns 'opened_at' and 'category'

# Convert 'opened_at' to datetime if it's not already
df['opened_at'] = pd.to_datetime(df['opened_at'])

# Extract date from 'opened_at'
df['date'] = df['opened_at'].dt.date

# Group by category and date, then count the number of incidents
category_daily = df.groupby(['category', 'date']).size().reset_index(name='counts')

# Convert 'date' back to datetime for resampling
category_daily['date'] = pd.to_datetime(category_daily['date'])

# Prepare an empty DataFrame to hold resampled data
category_weekly = pd.DataFrame()

# Loop through each category to resample separately
for category in category_daily['category'].unique():
    temp_df = category_daily[category_daily['category'] == category]
    resampled_df = temp_df.set_index('date').resample('W').sum().reset_index()
    resampled_df['category'] = category  # add category column back after resampling
    category_weekly = pd.concat([category_weekly, resampled_df], ignore_index=True)

# Plot the trend for each category
plt.figure(figsize=(14, 7))
sns.lineplot(x='date', y='counts', hue='category', data=category_weekly, marker='o')
plt.title("Trend in Volume of Incident Tickets Per Week by Category")
plt.xlabel("Date")
plt.ylabel("Number of Incidents Opened")
plt.legend(title='Category')
plt.grid(True)
plt.show()
