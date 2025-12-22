import os
import json
import argparse
import requests
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pandas import date_range
# Identify potential duplicates based on user, amount, category, and short description
duplicate_entries = df[df.duplicated(subset=['user', 'amount', 'category', 'short_description'], keep=False)]

# Count the number of duplicates per user
duplicates_count = duplicate_entries['user'].value_counts()

# Plot the number of duplicate claims per user
plt.figure(figsize=(10, 6))
duplicates_count.plot(kind='bar', color='tomato')
plt.title('Number of Duplicate Expense Claims by User')
plt.xlabel('User')
plt.ylabel('Number of Duplicate Claims')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
