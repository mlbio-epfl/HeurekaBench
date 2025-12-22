import os
import json
import argparse
import requests
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pandas import date_range
# Calculate the distribution of expense categories
expense_categories_distribution = data['category'].value_counts().reset_index()
expense_categories_distribution.columns = ['category', 'count']

# Set the style of the visualization
sns.set(style="whitegrid")

# Create a bar plot for the distribution of expense categories
plt.figure(figsize=(12, 6))
sns.barplot(x='category', y='count', data=expense_categories_distribution)
plt.title('Distribution of Expense Categories')
plt.xlabel('Category')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.show()
