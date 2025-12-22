import os
import json
import argparse
import requests
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pandas import date_range
# Extract printer IDs from 'short_description' (assuming the printer ID is mentioned in the description)
df['printer_id'] = df['short_description'].str.extract('(Printer\d+)')
# Count the frequency of incidents for each printer ID
printer_counts = df['printer_id'].value_counts()
df_plot = printer_counts.reset_index()
df_plot.columns = ['Printer ID', 'Number of Incidents']

# # Define printer IDs if not present in short description
# printer_ids = ['Printer123', 'Printer456', 'Printer789', 'Printer321', 'Printer654']

# # Mock number of incidents for each printer
# printer_counts = [225, 5, 15, 10, 20]

# # Create a DataFrame from the counts for plotting
# df_plot = pd.DataFrame({'Printer ID': printer_ids, 'Number of Incidents': printer_counts})

# Plot the frequency
plot = df_plot.plot(kind='bar', x='Printer ID', y='Number of Incidents', legend=False, color='blue')

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
plt.title('Incidents by Printer ID')

# Set x-axis label
plt.xlabel('Printer ID')

# Set y-axis label
plt.ylabel('Number of Incidents')

# Display the figure
plt.show()
