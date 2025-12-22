import os
import json
import argparse
import requests
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pandas import date_range
# Convert 'end_date' to datetime format for easier manipulation
df['end_date'] = pd.to_datetime(df['end_date'])

# Define the fiscal year-end date and a range to consider "end of the fiscal year"
fiscal_year_end = '2023-03-31'
end_of_fiscal_year_range_start = pd.to_datetime(fiscal_year_end) - pd.DateOffset(months=3)  # 3 months before fiscal year end
end_of_fiscal_year_range_end = pd.to_datetime(fiscal_year_end)

# Filter projects ending near the fiscal year-end
end_of_year_projects = df[(df['end_date'] >= end_of_fiscal_year_range_start) &
                          (df['end_date'] <= end_of_fiscal_year_range_end)]

# Count projects by department in the filtered range
project_counts = end_of_year_projects['department'].value_counts()

# Plot the trend of projects by department towards the fiscal year-end
plt.figure(figsize=(10, 6))
project_counts.plot(kind='bar', color=['#4CAF50' if dept == 'Finance' else '#FFC107' for dept in project_counts.index])
plt.title('Number of Projects by Department Ending Near the Fiscal Year-End')
plt.xlabel('Department')
plt.ylabel('Number of Projects')
plt.xticks(rotation=45)
plt.grid(axis='y')

# Highlight the Finance department bar if it has a significant trend
if 'Finance' in project_counts and project_counts['Finance'] > project_counts.mean():
    plt.annotate(
        f"  {project_counts['Finance']} projects",
        xy=(project_counts.index.get_loc('Finance'), project_counts['Finance']),
        xytext=(project_counts.index.get_loc('Finance'), project_counts['Finance'] + 2),
        arrowprops=dict(facecolor='red', shrink=0.05),
        fontsize=12, color='red'
    )

plt.show()
