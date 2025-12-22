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

# Group the data by department and state and count occurrences
department_state_counts = flag_data.groupby(['department', 'state']).size().unstack(fill_value=0)

# Calculate proportions of each state within each department
department_state_proportions = department_state_counts.div(department_state_counts.sum(axis=1), axis=0)

# Plot the data, focusing only on the 'Declined' state
fig, ax = plt.subplots(figsize=(12, 8))
department_state_proportions['Declined'].plot(kind='bar', color='red', ax=ax)

# Add titles and labels
ax.set_title('Proportion of Declined Expenses by Department', fontsize=16)
ax.set_xlabel('Department', fontsize=14)
ax.set_ylabel('Proportion of Declined', fontsize=14)
ax.set_ylim(0, 1)  # Set y-axis limit to show proportions from 0 to 1

# Show grid
ax.grid(True)

# Rotate the x-axis labels for better readability
plt.xticks(rotation=45)
plt.tight_layout()  # Adjust layout to not cut off labels

# Adding numeric labels on top of the bars
for p in ax.patches:
    ax.annotate(f"{p.get_height():.2f}", (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='center', xytext=(0, 10), textcoords='offset points')

# Show the plot
plt.show()
