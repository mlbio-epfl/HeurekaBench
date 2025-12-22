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
dataset_path = "csvs/flag-9.csv"
# Load the dataset
df = pd.read_csv(dataset_path)
df = df[df['category'] == 'Hardware']
df['opened_at'] = pd.to_datetime(df['opened_at'])

# Count the number of hardware incidents per month
incident_counts = df.groupby(df['opened_at'].dt.to_period("M")).size().reset_index(name='counts')
incident_counts['date_ordinal'] = incident_counts['opened_at'].dt.start_time.apply(lambda x: x.toordinal())

# Prepare data for linear regression
X = incident_counts['date_ordinal'].values.reshape(-1, 1)  # Reshape for sklearn
y = incident_counts['counts'].values  # Target variable: number of incidents

# Fit the linear regression model
model = LinearRegression()
model.fit(X, y)

# Predict future values
future_dates = pd.date_range(start=incident_counts['opened_at'].max().to_timestamp(), periods=12, freq='M')  # Predicting for the next 10 years, monthly
future_dates_ordinal = [d.toordinal() for d in future_dates]
future_preds = model.predict(np.array(future_dates_ordinal).reshape(-1, 1))

# Plotting
plt.figure(figsize=(12, 6))
plt.scatter(incident_counts['opened_at'].dt.start_time, y, color='blue', label='Historical Hardware Incident Counts')
plt.scatter(future_dates, future_preds, color='red', label='Predicted Hardware Incident Trend')
plt.title('Projected Trends in Hardware Incidents')
plt.xlabel('Date')
plt.ylabel('Number of Hardware Incidents')
plt.legend()
plt.grid(True)

# Formatting the x-axis to make it more readable
plt.gca().xaxis.set_major_locator(mdates.YearLocator())
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
