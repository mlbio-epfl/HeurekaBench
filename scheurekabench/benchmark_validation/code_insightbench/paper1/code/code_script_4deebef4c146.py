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

# Assume 'goal_data' is your DataFrame and already loaded

# Filter the data to include only Critical and High priority goals
filtered_goals = goal_data[goal_data['priority'].isin(['Critical', 'High'])]

# Create a new column 'IT_or_Other' to distinguish between IT and other departments
filtered_goals['IT_or_Other'] = filtered_goals['department'].apply(lambda x: 'IT' if x == 'IT' else 'Other')

# Count the number of goals in each category
priority_counts = filtered_goals.groupby(['IT_or_Other', 'priority']).size().reset_index(name='counts')
# divide counts for other by 4 to get the average
priority_counts.loc[priority_counts['IT_or_Other'] == 'Other', 'counts'] = priority_counts['counts'] / 4

# Plotting
plt.figure(figsize=(10, 6))
bar_plot = sns.barplot(x='IT_or_Other', y='counts', hue='priority', data=priority_counts)
plt.title('Distribution of Critical and High Priority Goals: IT vs. Other Departments')
plt.xlabel('Department Category')
plt.ylabel('Number of Goals')
plt.legend(title='Priority')

# Annotate bars with the count of goals
for p in bar_plot.patches:
    bar_plot.annotate(format(p.get_height(), '.0f'),
                      (p.get_x() + p.get_width() / 2., p.get_height()),
                      ha='center', va='center',
                      xytext=(0, 9),
                      textcoords='offset points')

plt.show()
