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
import numpy as np

# Assuming 'flag_data' and 'data_user_human_agents' are already defined and preprocessed correctly
# Merge the expense data with user data to include employee start dates
merged_data = pd.merge(flag_data, data_user_human_agents, left_on='user', right_on='name', how='inner')

# Ensure 'opened_at' and 'start_date' are datetime objects
merged_data['opened_at'] = pd.to_datetime(merged_data['opened_at'], errors='coerce')
merged_data['start_date'] = pd.to_datetime(merged_data['start_date'], errors='coerce')

# Calculate the tenure in years at the time of expense submission
merged_data['tenure_years'] = (merged_data['opened_at'] - merged_data['start_date']).dt.days / 365.25

# Define tenure groups
tenure_bins = [0, 1, 3, 5, 10, np.inf]  # 0-1 year, 1-3 years, 3-5 years, 5-10 years, 10+ years
tenure_labels = ['<1 Year', '1-3 Years', '3-5 Years', '5-10 Years', '>10 Years']
merged_data['tenure_group'] = pd.cut(merged_data['tenure_years'], bins=tenure_bins, labels=tenure_labels)

# Filter for declined expenses
declined_data = merged_data[merged_data['state'] == 'Declined']

# Calculate the proportion of declined expenses within each tenure group
rejection_rates = declined_data.groupby('tenure_group').size() / merged_data.groupby('tenure_group').size()

# Plot the data
fig, ax = plt.subplots(figsize=(10, 6))
rejection_rates.plot(kind='bar', color='tomato', ax=ax)

# Add titles and labels
ax.set_title('Rejection Rates of Expenses by Employee Tenure', fontsize=16)
ax.set_xlabel('Employee Tenure', fontsize=14)
ax.set_ylabel('Rejection Rate', fontsize=14)
ax.set_ylim(0, 1)  # Set y-axis limit to show proportions from 0 to 1

# Show grid
ax.grid(True)

# Rotate the x-axis labels for better readability
plt.xticks(rotation=45)
plt.tight_layout()  # Adjust layout to prevent cutting off labels

# Show the plot
plt.show()
