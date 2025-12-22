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

# Convert opened_at and closed_at to datetime
df["opened_at"] = pd.to_datetime(df["opened_at"])
df["closed_at"] = pd.to_datetime(df["closed_at"])

# Compute resolution time in days
df["resolution_time"] = (df["closed_at"] - df["opened_at"]).dt.total_seconds() / 86400

# Extract month-year from opened_at and create a new column
df["month_year"] = df["opened_at"].dt.to_period("M")

# Group by month_year and category, then compute average resolution time
df_grouped = (
    df.groupby(["month_year", "assigned_to"])["resolution_time"].mean().unstack()
)

# Plot the data
df_grouped.plot(kind="line", figsize=(12, 6))
plt.title("Average Resolution Time by agent Over Time")
plt.xlabel("Month-Year")
plt.ylabel(" Resolution Time (days) over time")
plt.xticks(rotation=45)
plt.legend(title="Assigned_to")
plt.show()
