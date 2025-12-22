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
import pandas as pd

# Assuming 'flag_data' and 'data_user_human_agents' are already defined and preprocessed correctly
# Merge the expense data with user data to include employee start dates and department info
merged_data = pd.merge(flag_data, data_user_human_agents, left_on='user', right_on='name', how='inner')

# Convert 'opened_at' and 'start_date' to datetime objects
merged_data['opened_at'] = pd.to_datetime(merged_data['opened_at'], errors='coerce')
merged_data['start_date'] = pd.to_datetime(merged_data['start_date'], errors='coerce')

# Calculate tenure in years at the time of expense submission
merged_data['tenure_years'] = (merged_data['opened_at'] - merged_data['start_date']).dt.days / 365.25

# Filter for employees with less than 1 year of tenure
new_hires_data = merged_data[merged_data['tenure_years'] < 1]

# Group by department to get counts of declined and total reports
declined_counts = new_hires_data[new_hires_data['state'] == 'Declined'].groupby('department_y').size()
total_counts = new_hires_data.groupby('department_y').size()

# Prepare the DataFrame for plotting
plot_data = pd.DataFrame({
    'Declined': declined_counts,
    'Total Submitted': total_counts
}).fillna(0)  # Fill NaN values with 0 where there are no declines

# Create a bar plot for both declined and total submissions
fig, ax1 = plt.subplots(figsize=(12, 8))

plot_data.sort_values('Total Submitted', ascending=False).plot(kind='bar', ax=ax1, color=['red', 'blue'], alpha=0.75)

ax1.set_title('Expense Report Distribution for New Hires (<1 Year) by Department', fontsize=16)
ax1.set_xlabel('Department', fontsize=14)
ax1.set_ylabel('Number of Reports', fontsize=14)
ax1.grid(True)

plt.xticks(rotation=45)
plt.tight_layout()

plt.show()
