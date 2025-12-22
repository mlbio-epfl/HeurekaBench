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
import matplotlib.dates as mdates

# Assuming 'flag_data' and 'data_user_human_agents' are already defined and preprocessed correctly
# First, filter out expenses that were declined
declined_expenses = flag_data[flag_data['state'] == 'Declined']

# Merge this with user data to get corresponding start dates
merged_data = pd.merge(declined_expenses, data_user_human_agents, left_on='user', right_on='name', how='inner')

# Convert 'start_date' and 'opened_at' to datetime if not already
merged_data['start_date'] = pd.to_datetime(merged_data['start_date'], errors='coerce')
merged_data['opened_at'] = pd.to_datetime(merged_data['opened_at'], errors='coerce')

# Drop any rows where dates could not be converted (resulting in NaT)
merged_data.dropna(subset=['start_date', 'opened_at'], inplace=True)

# Check if there are any unrealistic dates (e.g., year 1970 often indicates a default Unix timestamp)
# and remove or correct them
merged_data = merged_data[(merged_data['start_date'].dt.year > 1970) & (merged_data['opened_at'].dt.year > 1970)]

# Create the scatter plot directly using datetime
plt.figure(figsize=(10, 6))
plt.scatter(merged_data['start_date'], merged_data['opened_at'], alpha=0.6, edgecolors='w', color='blue')
plt.title('Correlation Between User Start Date and Declined Expense Submission Date')
plt.xlabel('User Start Date')
plt.ylabel('Expense Declined Date')

# Set the formatter for the x and y axes to display dates properly
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.gca().yaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

# Ensure that the axes are using Date locators
plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
plt.gca().yaxis.set_major_locator(mdates.AutoDateLocator())

plt.grid(True)  # Enable grid for easier readability
plt.xticks(rotation=45)  # Rotate x-axis labels to make them more readable
plt.tight_layout()  # Adjust layout to prevent cutting off labels

plt.show()
