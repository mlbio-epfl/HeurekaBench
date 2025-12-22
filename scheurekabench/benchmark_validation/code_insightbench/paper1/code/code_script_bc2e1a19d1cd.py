import os
import json
import argparse
import requests
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pandas import date_range
# Filter for processed expenses and group by department
processed_expenses_by_department = data[data['state'] == 'Processed'].groupby('department').size().sort_values(ascending=False)

# Plotting
plt.figure(figsize=(10, 6))
processed_expenses_by_department.plot(kind='bar', color='dodgerblue')
plt.title('Number of Processed Expenses by Department')
plt.xlabel('Department')
plt.ylabel('Number of Processed Expenses')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
