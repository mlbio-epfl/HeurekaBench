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

# Filtering for Hardware category incidents
hardware_df = df[df['category'] == 'Hardware']

# Calculating TTR in days
hardware_df["ttr"] = (hardware_df["closed_at"] - hardware_df["opened_at"]).dt.total_seconds() / 86400

# Convert 'ttr' to numeric, handling errors
hardware_df["ttr"] = pd.to_numeric(hardware_df["ttr"], errors="coerce")

# Filtering data for the anomaly period
anomaly_period_df = hardware_df[(hardware_df['opened_at'] >= pd.Timestamp('2023-06-01')) &
                                (hardware_df['opened_at'] <= pd.Timestamp('2023-08-31'))]

# Create a lineplot to show TTR trends during the anomaly period
plt.figure(figsize=(12, 6))
sns.lineplot(data=anomaly_period_df, x="opened_at", y="ttr", hue="category")
plt.title("Time to Resolution (TTR) for Hardware Incidents During Anomaly Period")
plt.xlabel("Date")
plt.ylabel("Time to Resolution (days)")
plt.xticks(rotation=45)
plt.grid(True)
plt.legend(title='Category')
plt.tight_layout()
plt.show()
