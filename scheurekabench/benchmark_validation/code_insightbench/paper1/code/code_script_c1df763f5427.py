import os
import json
import argparse
import requests
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pandas import date_range
df = df[df['category'] == 'Hardware']
# Count the frequency of 'Printer' in 'short_description'
printer_incidents = df['short_description'].apply(lambda x: 'Printer' in x).sum()

# Create a DataFrame for plotting
df_plot = pd.DataFrame({'Keyword': ['Printer'], 'Frequency': [printer_incidents]})

# Plot the frequency
plot = df_plot.plot(kind='bar', x='Keyword', y='Frequency', legend=False, color='blue')

# Get the current figure for further manipulation
fig = plt.gcf()

# Loop through the rectangles (i.e., bars)
for i in plot.patches:
    # Get X and Y placement of label from rectangle
    x_value = i.get_x() + i.get_width() / 2
    y_value = i.get_height()

    # Use Y value as label and format number with one decimal place
    label = "{:.1f}".format(y_value)

    # Create annotation
    plt.annotate(
        label,                      # Use `label` as label
        (x_value, y_value),         # Place label at end of the bar
        xytext=(0, 5),              # Shift text slightly above bar
        textcoords="offset points", # Interpret `xytext` as offset in points
        ha='center',                # Horizontally align label
        va='bottom'                 # Vertically align label at bottom
    )

# Set plot title
plt.title('Frequency of Printer in Incident Descriptions')

# Set x-axis label
plt.xlabel('Keyword')

# Set y-axis label
plt.ylabel('Frequency')

# Display the figure
plt.show()
