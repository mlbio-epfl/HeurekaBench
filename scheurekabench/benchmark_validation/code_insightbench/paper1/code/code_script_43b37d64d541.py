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

# Assuming df is the DataFrame containing your incidents data

# Convert opened_at and closed_at to datetime
df["opened_at"] = pd.to_datetime(df["opened_at"])
df["closed_at"] = pd.to_datetime(df["closed_at"])

# Compute resolution time in days
df["resolution_time"] = (df["closed_at"] - df["opened_at"]).dt.total_seconds() / 86400

# Calculate the average resolution time for each category
avg_resolution_time_per_category = df.groupby('category')['resolution_time'].mean()

# Plotting the histogram
plt.figure(figsize=(10, 6))
avg_resolution_time_per_category.plot(kind='bar', color='skyblue')
plt.title('Average Time to Resolution Per Category')
plt.xlabel('Category')
plt.ylabel('Average Resolution Time (days)')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Show the plot
plt.show()
