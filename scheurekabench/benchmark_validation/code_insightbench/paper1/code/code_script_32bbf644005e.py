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
# Sort the DataFrame by the opened_at column
df = df.sort_values("opened_at")
df["opened_at"] = pd.to_datetime(df["opened_at"])
df["closed_at"] = pd.to_datetime(df["closed_at"])

# Create a new column 'month_year' to make the plot more readable
# df['month_year'] = df['opened_at'].dt.to_period('M')
df["ttr"] = (df["closed_at"] - df["opened_at"]).dt.total_seconds() / 86400
# Convert 'ttr' column to numeric and handle errors
df["ttr"] = pd.to_numeric(df["ttr"], errors="coerce")

# Create a lineplot
plt.figure(figsize=(12, 6))
sns.lineplot(data=df, x="opened_at", y="ttr", hue="category")
plt.title("Time to Resolution (TTR) Over Time for Different Categories")
plt.xticks(rotation=45)
plt.show()
