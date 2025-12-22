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
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from sklearn.linear_model import LinearRegression

# Load data
dataset_path = "csvs/flag-6.csv"
df = pd.read_csv(dataset_path)
df = df[df['assigned_to'] == 'Fred Luddy']
df['opened_at'] = pd.to_datetime(df['opened_at'])
df['closed_at'] = pd.to_datetime(df['closed_at'])

# Compute resolution time in days
df["resolution_time"] = (df["closed_at"] - df["opened_at"]).dt.total_seconds() / 86400
# Remove rows with NaN values in 'resolution_time'
df = df.dropna(subset=['resolution_time'])
# Convert dates to ordinal for regression analysis
df['date_ordinal'] = df['opened_at'].apply(lambda x: x.toordinal())

# Prepare data for linear regression
X = df['date_ordinal'].values.reshape(-1, 1)  # Reshape for sklearn
y = df['resolution_time'].values  # Target variable

# Fit the linear regression model
model = LinearRegression()
model.fit(X, y)

# Predict future values
future_dates = pd.date_range(start=df['opened_at'].max(), periods=120, freq='D')  # 4 months into the future
future_dates_ordinal = [d.toordinal() for d in future_dates]
future_preds = model.predict(np.array(future_dates_ordinal).reshape(-1, 1))

# Plotting
plt.figure(figsize=(12, 6))
plt.scatter(df['opened_at'], df['resolution_time'], color='blue', label='Historical TTR')
plt.plot(future_dates, future_preds, color='red', linestyle='--', label='Predicted TTR Trend')
plt.title('Projected Increase in TTR for Fred Luddy')
plt.xlabel('Date')
plt.ylabel('Time to Resolution (days)')
plt.legend()
plt.grid(True)

# Formatting the x-axis to make it more readable
plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
