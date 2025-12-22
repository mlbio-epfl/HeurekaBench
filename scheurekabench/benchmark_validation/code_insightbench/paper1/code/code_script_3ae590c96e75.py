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

# Assuming 'goal_data' is preloaded and contains 'Cost Reduction' category
goal_data['end_date'] = pd.to_datetime(goal_data['end_date'])
goal_data["start_date"] = pd.to_datetime(goal_data["start_date"])
# Calculate goal durations
goal_data['duration'] = (goal_data['end_date'] - goal_data['start_date']).dt.days

# Plotting
plt.figure(figsize=(12, 8))
box_plot = sns.boxplot(x='department', y='duration', data=goal_data, palette="Set3")
plt.title('Comparison of Goal Durations by Department')
plt.xlabel('Department')
plt.ylabel('Goal Duration (days)')
plt.grid(True)

# Calculate median and mean for annotations
medians = goal_data.groupby(['department'])['duration'].median()
means = goal_data.groupby(['department'])['duration'].mean()

# Iterate over the departments to place the text annotations for median and mean
for xtick in box_plot.get_xticks():
    box_plot.text(xtick, medians[xtick] + 1, 'Median: {:.1f}'.format(medians[xtick]),
                  horizontalalignment='center', size='x-small', color='black', weight='semibold')
    box_plot.text(xtick, means[xtick] + 1, 'Mean: {:.1f}'.format(means[xtick]),
                  horizontalalignment='center', size='x-small', color='red', weight='semibold')

plt.show()
