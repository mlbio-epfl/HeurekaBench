import os
import json
import argparse
import requests
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pandas import date_range
# Group by department and sum the amount
total_expenses_by_department = data.groupby('department')['amount'].sum().sort_values(ascending=False)

# Plotting
plt.figure(figsize=(10, 6))
total_expenses_by_department.plot(kind='bar', color='lightcoral')
plt.title('Total Expenses by Department')
plt.xlabel('Department')
plt.ylabel('Total Expenses ($)')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
