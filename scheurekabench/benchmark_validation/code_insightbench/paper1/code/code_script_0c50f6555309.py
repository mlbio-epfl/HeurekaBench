import os
import json
import argparse
import requests
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pandas import date_range
# Function to categorize descriptions based on keywords
def categorize_description(description):
    keywords = {"Travel": 1.5, "Service": 1.2, "Cloud": 1.3, "Asset": 0.8, "Equipment": 0.9}
    for keyword in keywords.keys():
        if pd.notnull(description) and keyword.lower() in description.lower():
            return keyword
    return 'Other'

# Apply the function to create a new column for categories
data['description_category'] = data['short_description'].apply(categorize_description)

# Set the style of the visualization
sns.set(style="whitegrid")

# Create a boxplot for amount by description category
plt.figure(figsize=(12, 6))
sns.boxplot(x='description_category', y='amount', data=data)
plt.title('Amount Distribution by Short Description Category')
plt.xlabel('Short Description Category')
plt.ylabel('Amount')
plt.xticks(rotation=45)
plt.show()
