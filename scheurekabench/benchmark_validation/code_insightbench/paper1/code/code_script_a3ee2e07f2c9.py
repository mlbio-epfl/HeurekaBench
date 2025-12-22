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

# Group by user, category, and amount to count occurrences
grouped_data = flag_data.groupby(['user', 'category', 'amount']).size().reset_index(name='frequency')

# Filter out normal entries to focus on potential anomalies
potential_fraud = grouped_data[grouped_data['frequency'] > 1]  # Arbitrary threshold, adjust based on your data

# Plot histogram of frequencies
plt.figure(figsize=(10, 6))
plt.hist(potential_fraud['frequency'], bins=30, color='red', alpha=0.7)
plt.title('Distribution of Repeated Claims Frequency')
plt.xlabel('Frequency of Same Amount Claims by Same User in Same Category')
plt.ylabel('Count of Such Incidents')
plt.grid(True)
plt.show()
