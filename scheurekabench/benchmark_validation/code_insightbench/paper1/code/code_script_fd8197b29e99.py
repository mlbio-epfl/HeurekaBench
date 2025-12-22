import os
import json
import argparse
import requests
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pandas import date_range
import matplotlib.pyplot as plt

# Assuming 'df' is the DataFrame containing your data
df["warranty_expiration"] = pd.to_datetime(df["warranty_expiration"])
df["purchased_on"] = pd.to_datetime(df["purchased_on"])
# Calculate the warranty period in years
df['warranty_period_years'] = (df['warranty_expiration'] - df['purchased_on']).dt.days / 365

# Create the scatter plot
plt.figure(figsize=(10, 6))
plt.scatter(df['purchased_on'], df['warranty_period_years'], alpha=0.6, edgecolors='w', color='blue')
plt.title('Correlation between purchased date and Warranty Period')
plt.xlabel('Purchased On Date')
plt.ylabel('Warranty Period (Years)')
plt.grid(True)

plt.show()
