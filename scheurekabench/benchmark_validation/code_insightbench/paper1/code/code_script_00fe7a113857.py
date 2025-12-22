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

# Assume flag_data includes 'user', 'amount', 'category' columns
# Group data by user, category, and amount to count frequencies
grouped_data = flag_data.groupby(['user', 'category', 'amount']).size().reset_index(name='count')

# Filter to only include cases with more than one claim (to highlight potential fraud)
repeated_claims = grouped_data[grouped_data['count'] > 1]

# Create a scatter plot with sizes proportional to the count of claims
plt.figure(figsize=(14, 8))
colors = {'Travel': 'blue', 'Meals': 'green', 'Accommodation': 'red', 'Miscellaneous': 'purple'}  # Add more categories as needed
for ct in repeated_claims['category'].unique():
    subset = repeated_claims[repeated_claims['category'] == ct]
    plt.scatter(subset['user'], subset['amount'], s=subset['count'] * 100,  # Increased size factor for better visibility
                color=colors.get(ct, 'gray'), label=f'Category: {ct}', alpha=0.6)

# Customizing the plot
plt.title('Repeated Expense Claims by User and Category')
plt.xlabel('User')
plt.ylabel('Amount ($)')
plt.legend(title='Expense Categories')
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
plt.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.7)

# Highlighting significant cases
# Let's annotate the specific user found in your description
for i, row in repeated_claims.iterrows():
    if row['user'] == 'Mamie Mcintee' and row['amount'] == 8000:
        plt.annotate(f"{row['user']} (${row['amount']})", (row['user'], row['amount']),
                     textcoords="offset points", xytext=(0,10), ha='center', fontsize=9, color='darkred')

# Show plot
plt.show()
