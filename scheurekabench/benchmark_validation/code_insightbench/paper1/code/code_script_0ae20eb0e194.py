import os
import json
import argparse
import requests
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pandas import date_range
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Filter data to include only 'Cost Reduction' category
cost_reduction_goals = goal_data[goal_data['category'] == 'Cost Reduction']

# Convert start_date to numerical days since the first date in the dataset for regression analysis
cost_reduction_goals['start_date_numeric'] = (cost_reduction_goals['start_date'] - cost_reduction_goals['start_date'].min()).dt.days

# Prepare data for plotting
cost_reduction_goals['duration'] = (cost_reduction_goals['end_date'] - cost_reduction_goals['start_date']).dt.days

# Plotting
plt.figure(figsize=(12, 8))
sns.scatterplot(x='start_date_numeric', y='duration', data=cost_reduction_goals, color='blue', label='Duration per Start Date')

# Convert numeric dates back to dates for labeling on x-axis
label_dates = pd.date_range(start=cost_reduction_goals['start_date'].min(), periods=cost_reduction_goals['start_date_numeric'].max()+1, freq='D')
plt.xticks(ticks=range(0, cost_reduction_goals['start_date_numeric'].max()+1, 50),  # Adjust ticks frequency as needed
           labels=[date.strftime('%Y-%m-%d') for date in label_dates[::50]])

sns.regplot(x='start_date_numeric', y='duration', data=cost_reduction_goals, scatter=False, color='red', label='Trend Line')

plt.title('Trend of Duration for Cost Reduction Goals Over Time')
plt.xlabel('Start Date')
plt.ylabel('Duration (days)')
plt.legend()
plt.show()
