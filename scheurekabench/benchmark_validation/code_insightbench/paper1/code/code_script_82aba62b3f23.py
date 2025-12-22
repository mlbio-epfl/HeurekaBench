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

# Group by department and calculate the average processing time for processed expenses
average_processing_time_by_department = df[df['state'] == 'Processed'].groupby('department')['processing_time_hours'].mean().sort_values()

# Plotting
plt.figure(figsize=(10, 6))
average_processing_time_by_department.plot(kind='bar', color='purple')
plt.title('Average Processing Time by Department')
plt.xlabel('Department')
plt.ylabel('Average Processing Time (Hours)')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
