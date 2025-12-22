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

# Group the data by category and state, then count occurrences
category_state_counts = flag_data.groupby(['category', 'state']).size().unstack(fill_value=0)

# Calculate proportions of each state within each category
category_state_proportions = category_state_counts.div(category_state_counts.sum(axis=1), axis=0)

# Plot the data, focusing only on the 'Declined' state
fig, ax = plt.subplots(figsize=(12, 8))
declined_proportions = category_state_proportions['Declined']
declined_proportions.plot(kind='bar', color='red', ax=ax)

# Add titles and labels
ax.set_title('Proportion of Declined Expenses by Category', fontsize=16)
ax.set_xlabel('Expense Category', fontsize=14)
ax.set_ylabel('Proportion of Declined', fontsize=14)
ax.set_ylim(0, 1)  # Set y-axis limit to show proportions from 0 to 1

# Show grid
ax.grid(True, which='both', linestyle='--', linewidth=0.5)

# Rotate the x-axis labels for better readability
plt.xticks(rotation=45)
plt.tight_layout()  # Adjust layout to not cut off labels

# Adding numeric labels on top of the bars
for i, value in enumerate(declined_proportions):
    ax.text(i, value, f"{value:.2f}", ha='center', va='bottom', fontsize=10, color='black')

# Show the plot
plt.show()
