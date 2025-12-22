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

# Assuming 'flag_data' contains 'department', 'category', and 'processing_period' columns
# Calculate processing period in days if not already calculated
flag_data['processed_date'] = pd.to_datetime(flag_data['processed_date'])
flag_data['opened_at'] = pd.to_datetime(flag_data['opened_at'])
flag_data['processing_period'] = (flag_data['processed_date'] - flag_data['opened_at']).dt.days

# Group data by department and category to count frequencies and calculate average processing time
category_counts = flag_data.groupby(['department', 'category']).size().reset_index(name='count')
category_processing_times = flag_data.groupby(['department', 'category'])['processing_period'].mean().reset_index()

# Merging counts with processing times for richer insights
category_data = pd.merge(category_counts, category_processing_times, on=['department', 'category'])

# Pivoting data for better visualization in stacked bar plot
pivot_data = category_data.pivot(index='department', columns='category', values='count').fillna(0)

# Plotting
plt.figure(figsize=(14, 8))
pivot_data.plot(kind='bar', stacked=True, colormap='viridis', alpha=0.7)
plt.title('Distribution of Expense Categories by Department with Processing Times')
plt.xlabel('Department')
plt.ylabel('Count of Expenses')
plt.xticks(rotation=45)
plt.legend(title='Expense Categories')

# Show mean processing times on bars for additional context
for n, x in enumerate([*pivot_data.index.values]):
    for (category, count), y in zip(pivot_data.loc[x].items(), pivot_data.loc[x].cumsum()):
        plt.text(n, y - (count / 2), f'{category_processing_times.loc[(category_processing_times["department"] == x) & (category_processing_times["category"] == category), "processing_period"].values[0]:.1f} days',
                 ha='center', va='center', color='black', fontweight='bold', fontsize=9)

plt.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.7)
plt.show()
