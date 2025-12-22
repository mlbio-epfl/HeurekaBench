import os
import json
import argparse
import requests
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pandas import date_range
# Filter data for relevant categories (Server and Web Server)
expensive_assets = flag_data[flag_data['model_category'].isin(['Server', 'Web Server'])]

# Count the number of each category within each department
category_counts = expensive_assets.groupby(['department', 'model_category']).size().unstack(fill_value=0).reset_index()

# Create a bar plot showing the counts of Server and Web Server by department
plt.figure(figsize=(12, 8))
sns.barplot(data=category_counts.melt(id_vars=["department"], var_name="model_category", value_name="count"),
            x='department', y='count', hue='model_category', palette="viridis")
plt.title('Distribution of Expensive Assets (Server and Web Server) by Department')
plt.xlabel('Department')
plt.ylabel('Count of Expensive Assets')
plt.xticks(rotation=45)

# Emphasize the HR department by changing the color of its bars
for bar in plt.gca().patches:
    if bar.get_x() == category_counts.index[category_counts['department'] == 'HR'][0]:
        bar.set_color('red')  # Change color to red for HR department

plt.legend(title='Asset Category')
plt.tight_layout()
plt.show()
