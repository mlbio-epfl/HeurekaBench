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
import numpy as np

# Assuming 'goal_data' is the DataFrame created from the previous code

# Calculate if each goal met its target percentage
goal_data['goal_met'] = goal_data.apply(lambda row: row['percent_complete'] >= row['target_percentage'], axis=1)

# Group by department and calculate the percentage of goals met
department_goal_achievement = goal_data.groupby('department')['goal_met'].mean() * 100

# Reset index to turn the series into a DataFrame
department_goal_achievement = department_goal_achievement.reset_index()

# Rename columns for better readability in the plot
department_goal_achievement.columns = ['Department', 'Percentage of Goals Met']

# Create a bar plot
plt.figure(figsize=(10, 6))
bar_plot = sns.barplot(x='Department', y='Percentage of Goals Met', data=department_goal_achievement, palette='viridis')
plt.title('Percentage of Target Goals Achieved by Department')
plt.xlabel('Department')
plt.ylabel('Percentage of Goals Met')
plt.ylim(0, 100)  # Set y-axis limits to make differences more evident
for p in bar_plot.patches:
    bar_plot.annotate(format(p.get_height(), '.0f'),
                      (p.get_x() + p.get_width() / 2., p.get_height()),
                      ha = 'center', va = 'center',
                      xytext = (0, 9),
                      textcoords = 'offset points')
plt.show()
