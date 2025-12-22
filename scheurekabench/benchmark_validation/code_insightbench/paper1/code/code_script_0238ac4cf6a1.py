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

# Create a new column 'month_year' to make the plot more readable
df["month_year"] = df["opened_at"].dt.to_period("M")

# Create a countplot
plt.figure(figsize=(12, 6))
sns.countplot(data=df, x="month_year", hue="location")
plt.title("Number of Incidents Created Over Location")
plt.xticks(rotation=45)
plt.show()
