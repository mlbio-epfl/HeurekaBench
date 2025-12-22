import os
import json
import argparse
import requests
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pandas import date_range
# Filter the data for the IT department
it_department_data = flag_data[flag_data['department'] == 'IT']

# Group by manager and count the number of reportees
reportees_per_manager = it_department_data.groupby('manager').size().reset_index(name='num_reportees')

# Set the aesthetic style of the plots
sns.set_style("whitegrid")

# Create a bar plot
plt.figure(figsize=(8, 6))
bar_plot = sns.barplot(x='manager', y='num_reportees', data=reportees_per_manager, palette="muted")

# Add title and labels to the plot
plt.title('Number of Reportees for Managers in IT Department')
plt.xlabel('Manager')
plt.ylabel('Number of Reportees')

# Show the plot
plt.show()
