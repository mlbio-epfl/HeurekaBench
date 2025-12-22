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

# Assuming 'df' is your DataFrame containing the expense report data
# Calculate the frequency of different states for each expense amount range
expense_brackets = [0, 100, 500, 1000, 5000, np.inf]
labels = ['< $100', '$100 - $500', '$500 - $1000', '$1000 - $5000', '> $5000']
df['expense_bracket'] = pd.cut(df['amount'], bins=expense_brackets, labels=labels, right=False)

# Group by expense bracket and state, then count occurrences
state_distribution = df.groupby(['expense_bracket', 'state']).size().unstack().fillna(0)

# Plotting
fig, ax = plt.subplots(figsize=(12, 8))
bars = state_distribution.plot(kind='bar', stacked=True, ax=ax, color=['green', 'red', 'blue', 'orange'])

ax.set_title('Distribution of Expense Amounts by State', fontsize=16)
ax.set_xlabel('Expense Bracket', fontsize=14)
ax.set_ylabel('Number of Expenses', fontsize=14)
ax.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()

# Add number labels on top of each bar
for bar in bars.containers:
    ax.bar_label(bar, label_type='center')

plt.show()
