import os
import json
import argparse
import requests
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pandas import date_range
# Filter for only 'Computer' model_category
computers_data = flag_data[flag_data['model_category'] == 'Computer']

# Group by department and count the number of computers
department_computer_counts = computers_data.groupby('department').size()

# Count the number of unique users in each department
department_user_counts = flag_data.groupby('department')['assigned_to'].nunique()

# Calculate the average number of computers per user in each department
average_computers_per_user = department_computer_counts / department_user_counts
average_computers_per_user = average_computers_per_user.reset_index(name='Average Number of Computers per User')

# Plotting using seaborn and matplotlib
plt.figure(figsize=(10, 6))
sns.barplot(x='department', y='Average Number of Computers per User', data=average_computers_per_user)
plt.xticks(rotation=45)
plt.title('Average Number of Computers per User Across Departments')
plt.xlabel('Department')
plt.ylabel('Average Number of Computers per User')
plt.tight_layout()  # Adjusts plot to ensure everything fits without overlap
plt.show()
