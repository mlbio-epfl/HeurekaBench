import os
import json
import argparse
import requests
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pandas import date_range
# Group by department and count unique managers
department_manager_counts = flag_data.groupby('department')['manager'].nunique().reset_index()

# Set the aesthetic style of the plots
sns.set_style("whitegrid")

# Create a bar plot
plt.figure(figsize=(10, 6))
bar_plot = sns.barplot(x='department', y='manager', data=department_manager_counts, palette="muted")

# Add title and labels to the plot
plt.title('Number of Unique Managers per Department')
plt.xlabel('Department')
plt.ylabel('Number of Unique Managers')

# Optional: add the exact number on top of each bar
for p in bar_plot.patches:
    bar_plot.annotate(format(p.get_height(), '.0f'),
                      (p.get_x() + p.get_width() / 2., p.get_height()),
                      ha = 'center', va = 'center',
                      xytext = (0, 9),
                      textcoords = 'offset points')

# Show the plot
plt.show()
