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

# Calculate goal durations in days
goal_data['duration'] = (goal_data['end_date'] - goal_data['start_date']).dt.days

# Plotting
plt.figure(figsize=(14, 8))
box_plot = sns.boxplot(x='category', y='duration', data=goal_data)
plt.title('Comparison of Goal Duration by Category Across All Departments')
plt.xlabel('Goal Category')
plt.ylabel('Duration (days)')
plt.xticks(rotation=45)  # Rotate category names for better readability
plt.grid(True)

# Calculate median and mean for annotations
medians = goal_data.groupby(['category'])['duration'].median()
means = goal_data.groupby(['category'])['duration'].mean()

# Iterate over the departments to place the text annotations for median and mean
for xtick in box_plot.get_xticks():
    box_plot.text(xtick, medians[xtick] + 1, 'Median: {:.1f}'.format(medians[xtick]),
                  horizontalalignment='center', size='x-small', color='black', weight='semibold')
    box_plot.text(xtick, means[xtick] + 1, 'Mean: {:.1f}'.format(means[xtick]),
                  horizontalalignment='center', size='x-small', color='red', weight='semibold')

plt.show()
