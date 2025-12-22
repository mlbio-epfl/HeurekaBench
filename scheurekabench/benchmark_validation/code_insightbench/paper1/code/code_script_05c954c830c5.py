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

# Define bins for the expense amounts and labels for these bins
bins = [0, 1000, 3000, 6000, 9000]
labels = ['Low (<$1000)', 'Medium ($1000-$3000)', 'High ($3000-$6000)', 'Very High (>$6000)']
flag_data['amount_category'] = pd.cut(flag_data['amount'], bins=bins, labels=labels, right=False)

# Calculate the average processing time for each category
average_processing_time = flag_data.groupby('amount_category')['processing_time'].mean()

# Create the bar plot
plt.figure(figsize=(10, 6))
average_processing_time.plot(kind='bar', color='cadetblue')
plt.title('Average Processing Time by Expense Amount Category')
plt.xlabel('Expense Amount Category')
plt.ylabel('Average Processing Time (days)')
plt.xticks(rotation=45)  # Rotate labels to fit them better
plt.grid(True, axis='y')

# Show the plot
plt.show()
