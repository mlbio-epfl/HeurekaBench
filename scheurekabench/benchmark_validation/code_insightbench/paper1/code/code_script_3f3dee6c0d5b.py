import os
import json
import argparse
import requests
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pandas import date_range
# Group the data by 'assigned_to' and count the number of incidents for each agent
incident_counts = df.groupby('assigned_to').size()

# Find the agent with the maximum number of incidents
max_incidents_agent = incident_counts.idxmax()
max_incidents_count = incident_counts.max()

# Print the agent with the most incidents
print(f"The agent assigned the most incidents is {max_incidents_agent} with {max_incidents_count} incidents.")
