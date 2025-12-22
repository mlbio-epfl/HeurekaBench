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

# Assuming flag_data is your DataFrame containing expense data
# Group data by department and calculate total and average expenses
department_expenses = flag_data.groupby('department')['amount'].agg(['sum', 'mean']).reset_index()

# Sort data for better visualization (optional)
department_expenses.sort_values('sum', ascending=False, inplace=True)

# Creating the plot
fig, ax = plt.subplots(figsize=(14, 8))

# Bar plot for total expenses
# total_bars = ax.bar(department_expenses['department'], department_expenses['sum'], color='blue', label='Total Expenses')

# Bar plot for average expenses
average_bars = ax.bar(department_expenses['department'], department_expenses['mean'], color='green', label='Average Expenses', alpha=0.6, width=0.5)

# Add some labels, title and custom x-axis tick labels, etc.
ax.set_xlabel('Department')
ax.set_ylabel('Expenses ($)')
ax.set_title('Average Expenses by Department')
ax.set_xticks(department_expenses['department'])
ax.set_xticklabels(department_expenses['department'], rotation=45)
ax.legend()

# Adding a label above each bar
def add_labels(bars):
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.2f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

# add_labels(total_bars)
add_labels(average_bars)

plt.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.7)
plt.show()
