import os
import json
import argparse
import requests
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pandas import date_range
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Assume 'df' is your DataFrame containing the asset data
# Filter the DataFrame for only the HR department
hr_assets = df[df['department'] == 'HR']

# Convert the 'cost' column to numeric, just in case it's not already
hr_assets['cost'] = pd.to_numeric(hr_assets['cost'], errors='coerce')

# Calculate total and average cost per model category
total_cost = hr_assets.groupby('model_category')['cost'].sum().reset_index(name='Total Cost')
average_cost = hr_assets.groupby('model_category')['cost'].mean().reset_index(name='Average Cost')

# Merge the total and average cost dataframes
cost_data = pd.merge(total_cost, average_cost, on='model_category')

# Melt the dataframe to suit the seaborn barplot format for grouped bars
melted_cost_data = cost_data.melt(id_vars='model_category', var_name='Type of Cost', value_name='Cost')

# Create the bar plot
plt.figure(figsize=(14, 7))
avg_bar_plot = sns.barplot(data=melted_cost_data, x='model_category', y='Cost', hue='Type of Cost')

for p in avg_bar_plot.patches:
    avg_bar_plot.annotate(format(p.get_height(), '.2f'),
                          (p.get_x() + p.get_width() / 2., p.get_height()),
                          ha = 'center', va = 'center',
                          xytext = (0, 9),
                          textcoords = 'offset points')

plt.title('Total and Average Cost of Different Asset Types in HR Department')
plt.xlabel('Model Category')
plt.ylabel('Cost (USD)')
plt.xticks(rotation=45)
plt.legend(title='Type of Cost')
plt.show()
