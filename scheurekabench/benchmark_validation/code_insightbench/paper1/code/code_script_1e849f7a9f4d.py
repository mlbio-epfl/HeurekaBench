import os
import json
import argparse
import requests
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pandas import date_range
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
# Optionally, you can fit a linear regression line to emphasize the trend
# Using numpy for linear regression line
import numpy as np
# Convert dates to ordinal for regression
df['sys_updated_on_ordinal'] = df['purchased_on'].apply(lambda x: x.toordinal())
# Fit the regression
fit = np.polyfit(df['sys_updated_on_ordinal'], df['warranty_period_years'], 1)
fit_fn = np.poly1d(fit)
# Plot the regression line
plt.plot(df['purchased_on'], fit_fn(df['sys_updated_on_ordinal']), color='red', linewidth=2)
