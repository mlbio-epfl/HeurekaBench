import os
import json
import argparse
import requests
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pandas import date_range
# Group by department and calculate the average amount
average_expense_by_department = data.groupby('department')['amount'].mean().sort_values(ascending=False)

# Plotting
plt.figure(figsize=(10, 6))
average_expense_by_department.plot(kind='bar', color='goldenrod')
plt.title('Average Expense by Department')
plt.xlabel('Department')
plt.ylabel('Average Expense ($)')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
