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
import seaborn as sns
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

# Assuming 'goal_data' is preloaded and contains the relevant data for 'Cost Reduction' category
cost_reduction_goals = goal_data[goal_data['category'] == 'Cost Reduction']

# Convert start_date to a numeric value for regression (number of days since the first date)
cost_reduction_goals['start_date_numeric'] = (cost_reduction_goals['start_date'] - cost_reduction_goals['start_date'].min()).dt.days

# Calculate durations
cost_reduction_goals['duration'] = (cost_reduction_goals['end_date'] - cost_reduction_goals['start_date']).dt.days

# Prepare data for regression model
X = cost_reduction_goals[['start_date_numeric']]  # Features
y = cost_reduction_goals['duration']  # Target

# Fit the regression model
model = LinearRegression()
model.fit(X, y)

# Predict future durations
# Extend the date range by, say, 20% more time into the future for forecasting
future_dates = np.arange(X['start_date_numeric'].max() + 1, X['start_date_numeric'].max() * 1.2, dtype=int).reshape(-1, 1)
future_predictions = model.predict(future_dates)

# Plotting
plt.figure(figsize=(12, 8))
# Scatter plot for existing data
sns.scatterplot(x='start_date_numeric', y='duration', data=cost_reduction_goals, color='blue', label='Actual Durations')
# Regression line for existing data
sns.regplot(x='start_date_numeric', y='duration', data=cost_reduction_goals, scatter=False, color='red', label='Trend Line')
# Plot for future predictions
plt.plot(future_dates.flatten(), future_predictions, 'g--', label='Future Trend')
# Convert numeric dates back to actual dates for labeling on x-axis
actual_dates = pd.date_range(start=cost_reduction_goals['start_date'].min(), periods=int(1.2 * X['start_date_numeric'].max()), freq='D')
plt.xticks(ticks=range(0, int(1.2 * X['start_date_numeric'].max()), 50), labels=[date.strftime('%Y-%m-%d') for date in actual_dates[::50]], rotation=45)
plt.title('Future Trends in the Duration of \'Cost Reduction\' Goals')
plt.xlabel('Start Date')
plt.ylabel('Duration (days)')
plt.legend()
plt.grid(True)
plt.show()
