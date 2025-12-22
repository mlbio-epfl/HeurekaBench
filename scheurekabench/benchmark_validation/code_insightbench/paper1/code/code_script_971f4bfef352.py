import os
import json
import argparse
import requests
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pandas import date_range
# Convert start_date to datetime format
df['start_date'] = pd.to_datetime(df['start_date'])

# Extract the month and quarter from the start_date
df['month'] = df['start_date'].dt.month
df['quarter'] = df['start_date'].dt.quarter

# Visualize the trend of percent_complete by quarter
plt.figure(figsize=(12, 6))
sns.boxplot(x='quarter', y='percent_complete', data=df)
plt.title('Percent Complete by Quarter')
plt.xlabel('Quarter')
plt.ylabel('Percent Complete')
plt.grid(True, axis='y', linestyle='--', alpha=0.7)
plt.show()
