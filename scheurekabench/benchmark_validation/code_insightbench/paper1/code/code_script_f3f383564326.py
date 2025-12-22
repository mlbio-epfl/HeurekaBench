import os
import json
import argparse
import requests
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pandas import date_range
# Calculate average amount for each department
avg_amount_by_department = data.groupby('department')['amount'].mean().reset_index()

# Set the style of the visualization
sns.set(style="whitegrid")

# Create a bar plot for average amount by department
plt.figure(figsize=(12, 6))
sns.barplot(x='department', y='amount', data=avg_amount_by_department)
plt.title('Average Amount by Department')
plt.xlabel('Department')
plt.ylabel('Average Amount')
plt.xticks(rotation=45)
plt.show()
