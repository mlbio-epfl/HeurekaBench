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

# Load the combined dataset
combined_file_path = 'csvs/flag-44.csv'
data = pd.read_csv(combined_file_path)

# Convert the date columns to datetime type and calculate processing time
data['opened_at'] = pd.to_datetime(data['opened_at'])
data['processed_date'] = pd.to_datetime(data['processed_date'], errors='coerce')
data['processing_time_hours'] = (data['processed_date'] - data['opened_at']).dt.total_seconds() / 3600

# Calculate average processing time for each state
avg_processing_time_by_state = data.groupby('state')['processing_time_hours'].mean().reset_index()

# Set the style of the visualization
sns.set(style="whitegrid")

# Create a bar plot for average processing time by state
plt.figure(figsize=(12, 6))
sns.barplot(x='state', y='processing_time_hours', data=avg_processing_time_by_state)
plt.title('Average Processing Time by State')
plt.xlabel('State')
plt.ylabel('Average Processing Time (hours)')
plt.xticks(rotation=45)
plt.show()
