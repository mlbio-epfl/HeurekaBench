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

# Load the dataset
df = pd.read_csv('csvs/flag-36.csv')  # Replace with the correct path if needed

# Define cross-departmental keywords
cross_dept_keywords = ['collaborate', 'joint', 'integration', 'cross-departmental', 'partnership']

# Identify cross-departmental tasks
df['is_cross_departmental'] = df['description'].apply(
    lambda desc: any(keyword in desc.lower() for keyword in cross_dept_keywords)
)

# Calculate average completion and target percentage
avg_data = df.groupby('is_cross_departmental').agg({
    'percent_complete': 'mean',
    'target_percentage': 'mean'
}).reset_index()

# Rename columns for clarity
avg_data['is_cross_departmental'] = avg_data['is_cross_departmental'].map({True: 'Cross-Departmental', False: 'Non-Cross-Departmental'})

# Plot the average completion and target percentages
plt.figure(figsize=(10, 6))
sns.barplot(x='is_cross_departmental', y='value', hue='variable',
            data=pd.melt(avg_data, id_vars='is_cross_departmental', value_vars=['percent_complete', 'target_percentage']),
            palette='coolwarm')
plt.title('Completion and Target Achievement: Cross-Departmental vs Non-Cross-Departmental')
plt.xlabel('Task Type')
plt.ylabel('Percentage')
plt.ylim(0, 100)
plt.legend(title='Metric')
plt.grid(True, axis='y', linestyle='--', alpha=0.7)
plt.show()
