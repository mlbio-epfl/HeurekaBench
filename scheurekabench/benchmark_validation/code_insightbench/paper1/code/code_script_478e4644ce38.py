import os
import json
import argparse
import requests
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pandas import date_range
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Assuming df is already loaded and sorted by 'opened_at' as in the previous code

# Filter the DataFrame to include only Hardware incidents
hardware_df = df[df['category'] == 'Hardware']

# Create a new DataFrame grouping by 'month_year' to count incidents in each period
hardware_counts = hardware_df.groupby('month_year').size().reset_index(name='counts')

# Create a bar plot to visualize the number of Hardware incidents over time
plt.figure(figsize=(12, 6))
plot = sns.barplot(data=hardware_counts, x='month_year', y='counts', color='blue')
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
plt.title("Number of Hardware Incidents Over Time")
plt.xlabel("Month and Year")
plt.ylabel("Number of Incidents")
plt.xticks(rotation=45)
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.tight_layout()
plt.show()
