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

# Assuming df is the DataFrame containing your incidents data

# Convert opened_at and closed_at to datetime
df["opened_at"] = pd.to_datetime(df["opened_at"])
df["closed_at"] = pd.to_datetime(df["closed_at"])

# Compute resolution time in days
df["resolution_time"] = (df["closed_at"] - df["opened_at"]).dt.total_seconds() / 86400

# Extract date from 'opened_at'
df['date'] = df['opened_at'].dt.date

# Group by category and date, calculate average resolution time
resolution_data = df.groupby(['category', 'date'])['resolution_time'].mean().reset_index()

# Convert 'date' back to datetime for better plotting
resolution_data['date'] = pd.to_datetime(resolution_data['date'])

# Plotting
plt.figure(figsize=(14, 7))

# Use lineplot to visualize the average resolution time for each category over time
sns.lineplot(data=resolution_data, x='date', y='resolution_time', hue='category', marker='o')

# Enhancing the plot
plt.title('Average Resolution Time of Incidents Over Time by Category')
plt.xlabel('Date')
plt.ylabel('Average Resolution Time (days)')
plt.legend(title='Category')
plt.grid(True)

# Show plot
plt.show()
