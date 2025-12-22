import os
import json
import argparse
import requests
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pandas import date_range
# Define a list of keywords that might suggest cross-departmental goals
cross_dept_keywords = ["collaborate", "joint", "integration", "cross-departmental", "partnership"]

# Function to check if a description suggests cross-departmental goals
def is_cross_departmental(description):
    return any(keyword in description.lower() for keyword in cross_dept_keywords)

# Apply the function to create a new column indicating cross-departmental goals
df['is_cross_departmental'] = df['description'].apply(is_cross_departmental)

# Calculate the average percent_complete and target_percentage for cross-departmental and non-cross-departmental tasks
avg_data = df.groupby('is_cross_departmental').agg({
    'percent_complete': 'mean',
    'target_percentage': 'mean'
}).reset_index()

# Rename the values for clarity
avg_data['is_cross_departmental'] = avg_data['is_cross_departmental'].map({True: 'Cross-Departmental', False: 'Non-Cross-Departmental'})

# Plot the average percent_complete and target_percentage in a single bar plot
plt.figure(figsize=(14, 7))
barplot = sns.barplot(x='is_cross_departmental', y='value', hue='variable',
                      data=pd.melt(avg_data, id_vars='is_cross_departmental', value_vars=['percent_complete', 'target_percentage']),
                      palette='coolwarm')

# Annotate the bars with the actual values
for p in barplot.patches:
    barplot.annotate(f'{p.get_height():.2f}%',
                     (p.get_x() + p.get_width() / 2., p.get_height()),
                     ha='center', va='center',
                     xytext=(0, 10),
                     textcoords='offset points',
                     fontweight='bold')

plt.title('Average Completion and Target Percentage: Cross-Departmental vs Non-Cross-Departmental Tasks')
plt.xlabel('Task Type')
plt.ylabel('Percentage')
plt.ylim(0, 100)
plt.legend(title='Metric', loc='upper left')
plt.grid(True, axis='y', linestyle='--', alpha=0.7)
plt.show()
