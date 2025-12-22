import os
import json
import argparse
import requests
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pandas import date_range
df['opened_at'] = pd.to_datetime(df['opened_at'])
df['closed_at'] = pd.to_datetime(df['closed_at'])
# Define the current date for the analysis, simulate up to the last 'opened_at' date
current_date = df['opened_at'].max()

# Create a range of dates from the start to the current date
date_range = pd.date_range(start=df['opened_at'].min(), end=current_date, freq='D')

# Function to count open incidents per date
def count_open_incidents(date, agent_data):
    # Incidents that are opened on or before 'date' and are not closed or closed after 'date'
    open_incidents = agent_data[(agent_data['opened_at'] <= date) & ((agent_data['closed_at'].isna()) | (agent_data['closed_at'] > date))]
    return len(open_incidents)

# Initialize a DataFrame to store the results
open_incidents_data = pd.DataFrame()

# Loop through each agent to calculate their open incidents over time
for agent in df['assigned_to'].unique():
    agent_data = df[df['assigned_to'] == agent]
    open_counts = [count_open_incidents(date, agent_data) for date in date_range]
    temp_df = pd.DataFrame({
        'Date': date_range,
        'Open Incidents': open_counts,
        'Agent': agent
    })
    open_incidents_data = pd.concat([open_incidents_data, temp_df], ignore_index=True)

# Plotting the data
plt.figure(figsize=(14, 7))
sns.lineplot(data=open_incidents_data, x='Date', y='Open Incidents', hue='Agent', marker='o')
plt.title('Number of Open Incidents Over Time for Each Agent')
plt.xlabel('Date')
plt.ylabel('Open Incidents')
plt.xticks(rotation=45)
plt.grid(True)
plt.legend(title='Agent')
plt.show()
