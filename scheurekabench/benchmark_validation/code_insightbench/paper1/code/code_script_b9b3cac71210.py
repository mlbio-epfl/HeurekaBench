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

# Assuming df is the DataFrame loaded from your CSV file
# Load your data
# df = pd.read_csv('path_to_your_csv_file.csv')

# Convert 'opened_at' to datetime if it's not already
df['opened_at'] = pd.to_datetime(df['opened_at'])

# Extract year and month from 'opened_at' to create a 'Year-Month' column for grouping
df['Year-Month'] = df['opened_at'].dt.to_period('M')

# Group by both 'assigned_to' and 'Year-Month' and count the number of incidents
trend_data = df.groupby(['assigned_to', 'Year-Month']).size().unstack(fill_value=0)

# Plotting
fig, ax = plt.subplots(figsize=(15, 7))
trend_data.T.plot(kind='line', marker='o', ax=ax)  # Transpose to have time on the x-axis

# Enhancing the plot
plt.title('Trend of Incident Assignments for Each Agent Over Time')
plt.xlabel('Year-Month')
plt.ylabel('Number of Incidents')
plt.grid(True)
plt.legend(title='Agent')
plt.xticks(rotation=45)

# Show plot
plt.tight_layout()
plt.show()
