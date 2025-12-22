import os
import json
import argparse
import requests
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pandas import date_range
# Define a list of common keywords/phrases and the corresponding impact on `amount`
keywords = {
    "Travel": 1.5,  # Increase amount by 50% if "Travel" is in the description
    "Service": 1.2,  # Increase amount by 20% if "Service" is in the description
    "Cloud": 1.3,  # Increase amount by 30% if "Cloud" is in the description
    "Asset": 0.8,  # Decrease amount by 20% if "Asset" is in the description
    "Equipment": 0.9  # Decrease amount by 10% if "Equipment" is in the description
}

# Function to categorize descriptions based on keywords
def categorize_description(description):
    for keyword in keywords.keys():
        if pd.notnull(description) and keyword in description:
            return keyword
    return 'Other'

# Apply the function to create a new column for categories
df['description_category'] = df['short_description'].apply(categorize_description)

# Set the style of the visualization
sns.set(style="whitegrid")

# Create a single boxplot for amount by description category
plt.figure(figsize=(12, 6))
sns.boxplot(x='description_category', y='amount', data=df)
plt.title('Amount Distribution by Short Description Category')
plt.xlabel('Short Description Category')
plt.ylabel('Amount')
plt.xticks(rotation=45)
plt.show()
