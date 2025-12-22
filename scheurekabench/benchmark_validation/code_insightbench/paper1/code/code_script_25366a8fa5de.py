import os
import json
import argparse
import requests
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pandas import date_range
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Assuming df is already loaded and has the necessary columns
# Define the post-leave period (assuming leave ends on 2023-08-15)
post_leave_start_date = pd.to_datetime("2023-08-16")
data_end_date = df['opened_at'].max()

# Filter incidents that were opened after the leave period
post_leave_incidents = df[(df['opened_at'] > post_leave_start_date) & (df['opened_at'] <= data_end_date)]

# Count the number of incidents assigned to each agent in the post-leave period
post_leave_counts = post_leave_incidents['assigned_to'].value_counts().reset_index()
post_leave_counts.columns = ['Agent', 'Incident Count']

# Plotting
plt.figure(figsize=(10, 6))
sns.barplot(x='Agent', y='Incident Count', data=post_leave_counts, palette='viridis')
plt.title('Distribution of Incident Assignments Post Leave Period')
plt.xlabel('Agent')
plt.ylabel('Number of Incidents')
plt.xticks(rotation=45)
plt.show()
