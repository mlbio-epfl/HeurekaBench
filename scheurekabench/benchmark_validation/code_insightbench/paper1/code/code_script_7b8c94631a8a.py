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

# Assuming df is already loaded and sorted by 'opened_at' as in the previous code

# Filter the DataFrame to include only Hardware incidents
hardware_df = df[df['category'] == 'Hardware']

# Create a new DataFrame grouping by 'month_year' to count incidents in each period
hardware_counts = hardware_df.groupby('month_year').size().reset_index(name='counts')

# Create a bar plot to visualize the number of Hardware incidents over time
plt.figure(figsize=(12, 6))
sns.barplot(data=hardware_counts, x='month_year', y='counts', color='blue')
plt.title("Number of Hardware Incidents Over Time")
plt.xlabel("Month and Year")
plt.ylabel("Number of Incidents")
plt.xticks(rotation=45)
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.tight_layout()
plt.show()
