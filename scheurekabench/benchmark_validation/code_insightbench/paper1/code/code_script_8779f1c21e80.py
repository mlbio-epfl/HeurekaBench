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

# Filter the data for the IT department
it_goals = goal_data[goal_data['department'] == 'IT']

# Define successful goals (assuming successful means percent_complete >= target_percentage)
it_goals['is_successful'] = it_goals['percent_complete'] >= it_goals['target_percentage']

# Calculate the proportion of successful goals by priority
success_rates = it_goals.groupby('priority')['is_successful'].mean()

# Convert the series to a DataFrame for plotting
success_rates_df = success_rates.reset_index()

# Plotting
plt.figure(figsize=(10, 6))
bar_plot = sns.barplot(x='priority', y='is_successful', data=success_rates_df, order=['Critical', 'High', 'Medium', 'Low'])
plt.title('Proportion of Successful Goals by Priority in IT Department')
plt.xlabel('Priority')
plt.ylabel('Proportion of Successful Goals')
plt.ylim(0, 1)  # Set the limit to show proportions from 0 to 1

# Correctly format and annotate each bar with the proportion as a percentage
for p in bar_plot.patches:
    bar_plot.annotate(format(p.get_height(), '.1%'),  # Format as a percentage with one decimal
                      (p.get_x() + p.get_width() / 2., p.get_height()),
                      ha='center', va='center',
                      xytext=(0, 9),
                      textcoords='offset points')
plt.show()
