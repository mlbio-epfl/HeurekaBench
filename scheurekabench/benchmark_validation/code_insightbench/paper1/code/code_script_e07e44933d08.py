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
import pandas as pd

# Assuming 'df' is your DataFrame containing the expense report data
# Filter for expenses greater than $5000
high_cost_expenses = df[df['amount'] < 1000]

# Calculate processing time in days
high_cost_expenses['processing_time'] = (pd.to_datetime(high_cost_expenses['processed_date']) - pd.to_datetime(high_cost_expenses['opened_at'])).dt.days

# Plot for Departments
plt.figure(figsize=(12, 7))
plt.subplot(2, 1, 1)  # Two rows, one column, first subplot
department_processing = high_cost_expenses.groupby('department')['processing_time'].mean()
department_processing.plot(kind='bar', color='teal')
plt.title('Average Processing Time by Department for Expenses < $1000')
plt.ylabel('Average Processing Time (days)')
plt.xlabel('Department')
plt.xticks(rotation=45)
plt.grid(True)

# Plot for Users
plt.subplot(2, 1, 2)  # Two rows, one column, second subplot
user_processing = high_cost_expenses.groupby('user')['processing_time'].mean()
user_processing.plot(kind='bar', color='orange')
plt.title('Average Processing Time by User for Expenses < $1000')
plt.ylabel('Average Processing Time (days)')
plt.xlabel('User')
plt.xticks(rotation=45)
plt.grid(True)

plt.tight_layout()
plt.show()
