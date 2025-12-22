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

# Assuming 'flag_data' is your DataFrame with the expense report data
# Filter the data to include only IT department and declined expenses
it_expenses = flag_data[(flag_data['department'] == 'IT') & (flag_data['state'] == 'Declined')]

# Count occurrences of declined reports by each user in the IT department
user_declined_counts = it_expenses.groupby('user').size().sort_values(ascending=False)

# Create a bar plot of the counts
fig, ax = plt.subplots(figsize=(12, 8))
user_declined_counts.plot(kind='bar', color='crimson', ax=ax)

# Add titles and labels
ax.set_title('Number of Declined Expense Reports by User in IT Department', fontsize=16)
ax.set_xlabel('User', fontsize=14)
ax.set_ylabel('Number of Declined Reports', fontsize=14)

# Show grid
ax.grid(True)

# Rotate the x-axis labels for better readability
plt.xticks(rotation=45)
plt.tight_layout()  # Adjust layout to not cut off labels

# Show the plot
plt.show()
