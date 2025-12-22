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

# Convert start_date to datetime format
df['start_date'] = pd.to_datetime(df['start_date'])

# Extract the month and quarter from the start_date
df['month'] = df['start_date'].dt.month
df['quarter'] = df['start_date'].dt.quarter

# Calculate the average percent_complete by quarter
avg_completion_by_quarter = df.groupby('quarter')['percent_complete'].mean().reset_index()

# Plot the average completion by quarter
plt.figure(figsize=(10, 6))
sns.barplot(x='quarter', y='percent_complete', data=avg_completion_by_quarter, palette='viridis')
plt.title('Average Completion Rate by Quarter')
plt.xlabel('Quarter')
plt.ylabel('Average Completion Percentage')
plt.ylim(0, 100)
plt.grid(True, axis='y', linestyle='--', alpha=0.7)
plt.show()
