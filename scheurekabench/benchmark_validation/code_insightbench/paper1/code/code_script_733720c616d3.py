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

# Assuming 'df' is the DataFrame containing your data
flag_data['opened_at'] = pd.to_datetime(flag_data['opened_at'])
flag_data["processed_date"] = pd.to_datetime(flag_data["processed_date"])
# Calculate the difference in days between 'opened_at' and 'process_date'
flag_data['processing_time'] = (flag_data['processed_date'] - flag_data['opened_at']).dt.days

# Create a scatter plot of amount vs. processing time
plt.figure(figsize=(12, 7))
plt.scatter(flag_data['amount'], flag_data['processing_time'], alpha=0.6, edgecolors='w', color='blue')
plt.title('Processing Time vs. Expense Amount')
plt.xlabel('Expense Amount ($)')
plt.ylabel('Processing Time (days)')
plt.grid(True)

# Annotate some points with amount and processing time for clarity
for i, point in flag_data.sample(n=50).iterrows():  # Randomly sample points to annotate to avoid clutter
    plt.annotate(f"{point['amount']}$, {point['processing_time']}d",
                 (point['amount'], point['processing_time']),
                 textcoords="offset points",
                 xytext=(0,10),
                 ha='center')

plt.show()
