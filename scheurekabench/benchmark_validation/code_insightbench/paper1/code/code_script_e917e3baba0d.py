import os
import json
import argparse
import requests
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pandas import date_range
# Convert 'opened_at' to datetime
df['opened_at'] = pd.to_datetime(df['opened_at'])

# Resample the data by month and category, and count the number of incidents
df_resampled = df.groupby([pd.Grouper(key='opened_at', freq='M'), 'category']).size().unstack()

# Plot the resampled data
plot = df_resampled.plot(kind='line')

# Set plot title
plt.title('Incidents Over Time by Category')

# Set x-axis label
plt.xlabel('Time')

# Set y-axis label
plt.ylabel('Number of Incidents')

# Display the figure
plt.show()
