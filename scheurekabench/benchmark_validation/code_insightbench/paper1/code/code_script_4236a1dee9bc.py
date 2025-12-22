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

# Group data by department and calculate the average cost per department
department_costs = flag_data.groupby('department')['cost'].mean().reset_index()

# Sort the data for better visualization, highlighting the HR department
department_costs = department_costs.sort_values(by='cost', ascending=False)

# Set style for nicer aesthetics
sns.set_style("whitegrid")
# Create a bar plot using Matplotlib
plt.figure(figsize=(10, 6))
avg_bar_plot = sns.barplot(data=department_costs, x='department', y='cost', palette="coolwarm")
plt.title('Average Cost of Assets by Department')
plt.xlabel('Department')
plt.ylabel('Average Cost ($)')
plt.xticks(rotation=45)

# Plot
plt.figure(figsize=(10, 6))
# avg_bar_plot = sns.barplot(x='Department', y='Reportees', data=avg_reportees_per_dept, palette="coolwarm")

# Add exact numbers on top of the bars for clarity
for p in avg_bar_plot.patches:
    avg_bar_plot.annotate(format(p.get_height(), '.2f'),
                          (p.get_x() + p.get_width() / 2., p.get_height()),
                          ha = 'center', va = 'center',
                          xytext = (0, 9),
                          textcoords = 'offset points')
# Highlight the HR department

plt.tight_layout()
plt.show()
