import os
import json
import argparse
import requests
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pandas import date_range
df["opened_at"] = pd.to_datetime(df["opened_at"])
# Sort the DataFrame by the opened_at column
df["date"] = df["opened_at"].dt.date

# Count the number of incidents per day
df_daily_count = df.groupby("date").size().reset_index(name="counts")

# Count the number of incidents per day
df_daily_count["date"] = pd.to_datetime(df_daily_count["date"])

# Resample the data to get the weekly count of incidents
df_weekly_count = df_daily_count.resample("W", on="date").sum().reset_index()

# Plot the trend
plt.figure(figsize=(12, 6))
sns.lineplot(x="date", y="counts", data=df_weekly_count)
plt.title("Trend in Volume of Incident Tickets Per Week")
plt.xlabel("Date")
plt.ylabel("Number of Incidents opened")
plt.show()
