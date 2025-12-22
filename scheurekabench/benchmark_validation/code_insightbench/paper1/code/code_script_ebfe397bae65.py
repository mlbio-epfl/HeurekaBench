import os
import json
import argparse
import requests
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pandas import date_range
agent_incident_count = df.groupby('assigned_to')['number'].count()

# Plot the histogram
ax = agent_incident_count.plot(kind='bar', figsize=(10,6))

for p in ax.patches:
    ax.annotate(format(p.get_height(), '.2f'),
                (p.get_x() + p.get_width() / 2., p.get_height()),
                ha = 'center', va = 'center',
                xytext = (0, 9),
                textcoords = 'offset points')
plt.title('Number of Incidents Assigned Per Agent')
plt.xlabel('Agent')
plt.ylabel('Number of Incidents Assigned')
plt.grid(True)
plt.xticks(rotation=45)
plt.show()
