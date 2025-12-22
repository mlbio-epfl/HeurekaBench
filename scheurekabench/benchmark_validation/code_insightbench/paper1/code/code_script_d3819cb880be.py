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

# Count the number of expense reports per department
department_counts = flag_data['department'].value_counts()

# Plot the data
fig, ax = plt.subplots(figsize=(12, 8))
department_counts.plot(kind='bar', color='skyblue', ax=ax)

# Add titles and labels
ax.set_title('Number of Expense Reports by Department', fontsize=16)
ax.set_xlabel('Department', fontsize=14)
ax.set_ylabel('Number of Expense Reports', fontsize=14)

# Show grid
ax.grid(axis='y')  # Only horizontal grid lines for readability

# Rotate the x-axis labels for better readability
plt.xticks(rotation=45)
plt.tight_layout()  # Adjust layout to not cut off labels

# Adding numeric labels on top of the bars for clarity
for p in ax.patches:
    ax.annotate(f"{int(p.get_height())}", (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='bottom', xytext=(0, 10), textcoords='offset points')

# Show the plot
plt.show()
