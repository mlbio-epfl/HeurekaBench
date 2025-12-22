import os
import json
import argparse
import requests
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pandas import date_range
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Assuming 'flag_data' is the DataFrame that contains the entire asset dataset

# Filter for entries where 'model_category' is 'Computer'
computers_data = flag_data[flag_data['model_category'] == 'Computer']

# Group by 'department' and count the number of computers per department
computers_per_department = computers_data.groupby('department').size().reset_index(name='Total Computers')

# Group by 'department' and count unique users per department
users_per_department = flag_data.groupby('department')['assigned_to'].nunique().reset_index(name='Total Users')

# Merge the two dataframes on 'department'
department_summary = pd.merge(computers_per_department, users_per_department, on='department', how='outer')

# Fill any NaN values which might appear if there are departments with no computers or users
department_summary.fillna(0, inplace=True)

# Print the result
print(department_summary)

# Plotting
plt.figure(figsize=(12, 6))
sns.barplot(data=department_summary, x='department', y='Total Users', color='blue', label='Total Users')
# sns.barplot(data=department_summary, x='department', y='Total Computers', color='red', alpha=0.6, label='Total Computers')

plt.title('Number of Users and Computers per Department')
plt.xlabel('Department')
plt.ylabel('Count')
plt.legend(loc='upper right')
plt.xticks(rotation=45)  # Rotates the x-axis labels to make them more readable
plt.tight_layout()  # Adjusts plot parameters to give some padding
plt.show()
