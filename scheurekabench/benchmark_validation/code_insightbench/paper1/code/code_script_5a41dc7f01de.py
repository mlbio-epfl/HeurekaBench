import os
import json
import argparse
import requests
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pandas import date_range
most_recent_updates = flag_data.groupby('assigned_to')['sys_updated_on'].max().reset_index()

import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates  # for date formatting
# Assuming most_recent_updates is already defined as shown previously
# It contains 'assigned_to' and the most recent 'sys_updated_on'

# Merge most_recent_updates with data_user_human_agents to get start_dates aligned with sys_updated_on dates
visualization_data = pd.merge(most_recent_updates, data_user_human_agents[['name', 'start_date']],
                             left_on='assigned_to', right_on='name', how='left')

# Drop any rows with NaN values that might affect the visualization
visualization_data.dropna(subset=['start_date', 'sys_updated_on'], inplace=True)

# Convert dates to ordinal for plotting purposes
visualization_data["sys_updated_on"] = pd.to_datetime(visualization_data["sys_updated_on"])
visualization_data["start_date"] = pd.to_datetime(visualization_data["start_date"])
visualization_data['sys_updated_on_ordinal'] = visualization_data['sys_updated_on'].apply(lambda x: x.toordinal())
visualization_data['start_date_ordinal'] = visualization_data['start_date'].apply(lambda x: x.toordinal())

# Create the scatter plot using datetime directly
plt.figure(figsize=(12, 6))
plt.scatter(visualization_data['sys_updated_on'], visualization_data['start_date'], alpha=0.6, edgecolors='w', color='blue')
plt.title('Correlation between Most Recent System Update and User Start Date')
plt.xlabel('Most Recent System Update Date')
plt.ylabel('User Start Date')

# Format the date display on the x and y axes
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.gca().yaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

# Set the date tick labels on the x-axis to be rotated for better readability
plt.gcf().autofmt_xdate()  # Automatically format x-axis dates to fit them better

# Optionally rotate y-axis labels manually if needed (uncomment the next line if desired)
# plt.gca().set_yticklabels(plt.gca().get_yticks(), rotation=45)

plt.grid(True)  # Add a grid for easier visual estimation

plt.show()
