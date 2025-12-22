import os
import json
import argparse
import requests
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pandas import date_range
# Group by department and manager, and count the number of employees per manager
reportees_per_manager = flag_data.groupby(['department', 'manager']).size().reset_index(name='num_reportees')

# Calculate the average number of reportees per manager for each department
avg_reportees_per_manager = reportees_per_manager.groupby('department')['num_reportees'].mean().reset_index()

# Set the aesthetic style of the plots
sns.set_style("whitegrid")

# Create a bar plot
plt.figure(figsize=(10, 6))
bar_plot = sns.barplot(x='department', y='num_reportees', data=avg_reportees_per_manager, palette="muted")

# Add title and labels to the plot
plt.title('Average Number of Reportees per Manager by Department')
plt.xlabel('Department')
plt.ylabel('Average Number of Reportees per Manager')

# Optional: add the exact number on top of each bar
for p in bar_plot.patches:
    bar_plot.annotate(format(p.get_height(), '.1f'),
                      (p.get_x() + p.get_width() / 2., p.get_height()),
                      ha = 'center', va = 'center',
                      xytext = (0, 9),
                      textcoords = 'offset points')

# Show the plot
plt.show()
