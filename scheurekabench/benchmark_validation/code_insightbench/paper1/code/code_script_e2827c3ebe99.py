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

flag_data["warranty_expiration"] = pd.to_datetime(flag_data["warranty_expiration"])
flag_data["sys_updated_on"] = pd.to_datetime(flag_data["sys_updated_on"])
# Calculate the warranty period in years for each asset
flag_data['warranty_period_years'] = (flag_data['warranty_expiration'] - flag_data['sys_updated_on']).dt.days / 365

# Group by model_category and calculate the average warranty period
avg_warranty_by_category = flag_data.groupby('model_category')['cost'].mean()

# Plotting
a_plot = avg_warranty_by_category.plot(kind='bar', color='skyblue', figsize=(10, 6))
for p in a_plot.patches:
    a_plot.annotate(format(p.get_height(), '.2f'),
                          (p.get_x() + p.get_width() / 2., p.get_height()),
                          ha = 'center', va = 'center',
                          xytext = (0, 9),
                          textcoords = 'offset points')
plt.xlabel('Model Category')
plt.ylabel('Average Cost ($)')
plt.title('Average Cost by Model Category')
plt.xticks(rotation=45)
plt.tight_layout()  # Adjust layout to make room for the rotated x-axis labels

# Show the plot
plt.show()
