import os
import json
import argparse
import requests
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pandas import date_range
# Calculate the average percent_complete by department and metric
avg_completion_by_dept_metric = df.groupby(['department', 'priority'])['percent_complete'].mean().unstack().reset_index()

# Plot the average completion by department and metric
plt.figure(figsize=(14, 8))
avg_completion_by_dept_metric.set_index('department').plot(kind='bar', stacked=True, colormap='tab20', ax=plt.gca())
plt.title('Average Completion Rate by Department and Priority')
plt.xlabel('Department')
plt.ylabel('Average Completion Percentage')
plt.ylim(0, 100)
plt.grid(True, axis='y', linestyle='--', alpha=0.7)
plt.legend(title='Metric', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()
