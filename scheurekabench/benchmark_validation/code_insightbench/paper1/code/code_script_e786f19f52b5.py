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

# Assuming 'flag_data' contains 'department', 'amount', and 'processing_period' columns
# and is already loaded with the data

# Filter data to only include the Development department
dev_expenses = flag_data[flag_data['department'] == 'Development']

# Define the amount brackets
bins = [0, 100, 500, 1000, 5000, 10000, np.inf]
labels = ['< $100', '$100 - $500', '$500 - $1000', '$1000 - $5000', '$5000 - $10000', '> $10000']
dev_expenses['amount_bracket'] = pd.cut(dev_expenses['amount'], bins=bins, labels=labels)

# Calculate the proportion of expenses in each bracket
bracket_counts = dev_expenses['amount_bracket'].value_counts(normalize=True) * 100

# Create the box plot to visualize processing periods by amount brackets
fig, ax1 = plt.subplots(figsize=(14, 8))
sns.boxplot(x='amount_bracket', y='processing_period', data=dev_expenses, palette='coolwarm', ax=ax1)
ax1.set_title('Processing Period by Expense Amount Brackets in Development Department')
ax1.set_xlabel('Expense Amount Brackets')
ax1.set_ylabel('Processing Period (days)')
ax1.tick_params(axis='x', rotation=45)  # Rotate labels for better readability

# Create a twin axis to show the proportion of expenses on the same plot
ax2 = ax1.twinx()
ax2.plot(bracket_counts.index, bracket_counts.values, color='k', marker='o', linestyle='-', linewidth=2, markersize=8)
ax2.set_ylabel('Proportion of Expenses (%)')
ax2.set_ylim(0, 100)  # Limit y-axis for proportion to 100%
ax2.grid(False)  # Turn off grid for the secondary axis to avoid visual clutter

# Adding annotations for proportions
for i, val in enumerate(bracket_counts.values):
    ax2.text(i, val + 3, f'{val:.1f}%', color='black', ha='center', va='bottom', fontweight='bold')

plt.show()
