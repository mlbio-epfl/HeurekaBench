import os
import json
import argparse
import requests
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pandas import date_range
# Group by category and opened_at date, then calculate average ttr
category_ttr_trend = df.groupby(['category', df['opened_at'].dt.date])['ttr_days'].mean().reset_index()

# Plot the trend for each category
fig, ax = plt.subplots(figsize=(10,6))

for category in category_ttr_trend['category'].unique():
    ax.plot(category_ttr_trend[category_ttr_trend['category'] == category]['opened_at'],
            category_ttr_trend[category_ttr_trend['category'] == category]['ttr_days'],
            label=category)

plt.title('Trend of TTR Across Categories Over Time')
plt.xlabel('Opened At')
plt.ylabel('Average TTR (Days)')
plt.legend(loc='best')
plt.grid(True)
plt.show()
