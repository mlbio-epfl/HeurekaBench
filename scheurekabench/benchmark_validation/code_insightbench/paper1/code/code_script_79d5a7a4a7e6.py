import os
import json
import argparse
import requests
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pandas import date_range
# Calculate average completion by priority and category
avg_completion_by_priority_category = df.groupby(['priority', 'category'])['percent_complete'].mean().unstack().reset_index()

# Plot the average completion by priority and category
plt.figure(figsize=(12, 8))
avg_completion_by_priority_category.plot(kind='bar', x='priority', stacked=True, colormap='Set3', ax=plt.gca())
plt.title('Average Completion Rate by Priority and Category')
plt.xlabel('Priority Level')
plt.ylabel('Average Completion Percentage')
plt.ylim(0, 100)
plt.grid(True, axis='y', linestyle='--', alpha=0.7)
plt.legend(title='Category', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()
