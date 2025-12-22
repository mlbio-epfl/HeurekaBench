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

# Assuming dataset_path is defined and points to the correct CSV file
df = pd.read_csv(dataset_path)

# Convert opened_at and closed_at to datetime
df["opened_at"] = pd.to_datetime(df["opened_at"])
df["closed_at"] = pd.to_datetime(df["closed_at"])

# Compute TTR in days
df["resolution_time"] = (df["closed_at"] - df["opened_at"]).dt.total_seconds() / 86400

# Group by 'assigned_to' and compute the average resolution time for each agent
avg_ttr_by_agent = df.groupby("assigned_to")["resolution_time"].mean()

# Plotting the average TTR of each agent as a histogram
ax = avg_ttr_by_agent.plot(kind='bar', figsize=(10, 6), color='skyblue')

plt.title("Average Resolution Time (TTR) by Agent")
plt.xlabel("Agent")
plt.ylabel("Average Resolution Time (days)")
plt.xticks(rotation=45)

# Annotate each bar with its value
for p in ax.patches:
    ax.annotate(format(p.get_height(), '.2f'),
                (p.get_x() + p.get_width() / 2., p.get_height()),
                ha = 'center', va = 'center',
                xytext = (0, 9),
                textcoords = 'offset points')

plt.show()
