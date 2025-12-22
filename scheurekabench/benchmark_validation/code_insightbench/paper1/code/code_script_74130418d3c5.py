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
import seaborn as sns
import numpy as np

# Assuming 'flag_data' contains 'department', 'processed_date', and 'opened_at'
# Calculate processing period in days
flag_data['processing_period'] = (flag_data['processed_date'] - flag_data['opened_at']).dt.days

# Filtering out None values for processing_period for valid plotting
valid_data = flag_data.dropna(subset=['processing_period'])

# Creating the box plot with a color palette to differentiate departments
plt.figure(figsize=(14, 8))
palette = sns.color_palette("coolwarm", n_colors=len(valid_data['department'].unique()))  # Create a color palette
box_plot = sns.boxplot(x='department', y='processing_period', data=valid_data, palette=palette)

plt.title('Processing Period by Department')
plt.xlabel('Department')
plt.ylabel('Processing Period (days)')
plt.xticks(rotation=45)  # Rotate labels for better readability

# Add grid for easier analysis
plt.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.7)

# Calculate means and ensure they're aligned with the x-axis labels
means = valid_data.groupby(['department'])['processing_period'].mean()
labels = [tick.get_text() for tick in box_plot.get_xticklabels()]
vertical_offset = valid_data['processing_period'].mean() * 0.05  # Offset from mean for annotation

# Annotate mean values
for label in labels:
    mean_value = means[label]
    x_position = labels.index(label)
    box_plot.text(x_position, mean_value + vertical_offset, f'{mean_value:.1f}',
                  horizontalalignment='center', size='medium', color='black', weight='semibold')

plt.show()
