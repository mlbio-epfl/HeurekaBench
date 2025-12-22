import os
import json
import argparse
import requests
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pandas import date_range
# Calculate average amount for each location
avg_amount_by_location = data.groupby('location')['amount'].mean().reset_index()

# Set the style of the visualization
sns.set(style="whitegrid")

# Create a bar plot for average amount by location
plt.figure(figsize=(12, 6))
sns.barplot(x='location', y='amount', data=avg_amount_by_location, palette='viridis')
plt.title('Average Expense Amount by Location')
plt.xlabel('Location')
plt.ylabel('Average Amount')
plt.xticks(rotation=45)
plt.show()
