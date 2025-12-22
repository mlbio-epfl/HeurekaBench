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

# Convert 'schedule' back to datetime format for visualization
df['schedule'] = pd.to_datetime(df['schedule'], errors='coerce')

# Filter data to include only the high-retention and other locations
df['location_category'] = df['location'].apply(lambda loc: 'High Retention' if 'Tokyo' in str(loc) or 'London' in str(loc) else 'Other')

# Calculate the average schedule length by location category
df['tenure_days'] = (pd.Timestamp('2024-10-29')- df['schedule']).dt.days
avg_tenure_by_location = df.groupby('location_category')['tenure_days'].mean().reset_index()

# Plot the average tenure by location category
plt.figure(figsize=(10, 6))
sns.barplot(x='location_category', y='tenure_days', data=avg_tenure_by_location, palette='coolwarm')
plt.title('Average Employee Retention by Location Category')
plt.xlabel('Location Category')
plt.ylabel('Average Tenure (Days)')
plt.grid(True, axis='y', linestyle='--', alpha=0.7)
plt.show()
