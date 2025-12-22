import os
import json
import argparse
import requests
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pandas import date_range
# Calculate the average percent_complete by month
avg_completion_by_month = df.groupby(df['start_date'].dt.month)['percent_complete'].mean().reset_index()

# Plot the average completion by month
plt.figure(figsize=(10, 6))
sns.lineplot(x='start_date', y='percent_complete', data=avg_completion_by_month, marker='o')
plt.title('Average Completion Rate by Month')
plt.xlabel('Month')
plt.ylabel('Average Completion Percentage')
plt.ylim(0, 100)
plt.grid(True, axis='y', linestyle='--', alpha=0.7)
plt.show()
