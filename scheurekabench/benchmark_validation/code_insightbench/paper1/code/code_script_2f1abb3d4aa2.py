import os
import json
import argparse
import requests
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pandas import date_range
# Group by department and user, then calculate the average amount
average_expense_per_user = df.groupby(['department', 'user'])['amount'].mean().groupby('department').mean().sort_values(ascending=False)

# Plotting
plt.figure(figsize=(10, 6))
average_expense_per_user.plot(kind='bar', color='lightgreen')
plt.title('Average Expense per User by Department')
plt.xlabel('Department')
plt.ylabel('Average Expense per User ($)')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
