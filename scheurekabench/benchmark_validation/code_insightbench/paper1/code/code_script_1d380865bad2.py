import os
import json
import argparse
import requests
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pandas import date_range
# Calculate the number of expense reports submitted by each user
expense_reports_by_user = data['user'].value_counts().reset_index()
expense_reports_by_user.columns = ['user', 'number_of_reports']

# Set the style of the visualization
sns.set(style="whitegrid")

# Create a bar plot for the number of expense reports by user
plt.figure(figsize=(12, 6))
sns.barplot(x='user', y='number_of_reports', data=expense_reports_by_user)
plt.title('Number of Expense Reports by User')
plt.xlabel('User')
plt.ylabel('Number of Expense Reports')
plt.xticks(rotation=90)
plt.show()
