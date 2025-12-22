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

# Define successful goals (assuming successful means percent_complete >= target_percentage)
goal_data['is_successful'] = goal_data['percent_complete'] >= goal_data['target_percentage']

# Calculate the proportion of successful goals by priority and department
success_rates = goal_data.groupby(['department', 'priority'])['is_successful'].mean().reset_index()

# Plotting
plt.figure(figsize=(14, 8))
barplot = sns.barplot(x='department', y='is_successful', hue='priority', data=success_rates, hue_order=['Critical', 'High', 'Medium', 'Low'])

# Annotate each bar
for p in barplot.patches:
    barplot.annotate(format(p.get_height(), '.2f'),  # format as a percentage
                     (p.get_x() + p.get_width() / 2., p.get_height()),
                     ha = 'center', va = 'center',
                     size=9,
                     xytext = (0, 5),
                     textcoords = 'offset points')

plt.title('Proportion of Successful Goals by Priority Across Departments')
plt.xlabel('Department')
plt.ylabel('Proportion of Successful Goals')
plt.ylim(0, 1)  # Set the limit to show proportions from 0 to 1
plt.legend(title='Priority')
plt.show()
