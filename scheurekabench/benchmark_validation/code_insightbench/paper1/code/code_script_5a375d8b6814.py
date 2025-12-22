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

# Assuming 'flag_data' includes 'user', 'department', 'amount', 'category' columns
# and it's already loaded with the data

# Filter for the specific user
user_data = flag_data[flag_data['user'] == 'Mamie Mcintee']

# Group data by department and category to count frequencies
department_category_counts = user_data.groupby(['department', 'category']).size().unstack(fill_value=0)

# Plotting
plt.figure(figsize=(12, 7))
department_category_counts.plot(kind='bar', stacked=True, color=['blue', 'green', 'red', 'purple', 'orange'], alpha=0.7)
plt.title('Distribution of Expense Claims by Department and Category for Mamie Mcintee')
plt.xlabel('Department')
plt.ylabel('Number of Claims')
plt.xticks(rotation=0)  # Keep the department names horizontal for better readability
plt.legend(title='Expense Categories')
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.show()
