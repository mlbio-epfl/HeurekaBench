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

flag_data["warranty_expiration"] = pd.to_datetime(flag_data["warranty_expiration"])
flag_data["purchased_on"] = pd.to_datetime(flag_data["purchased_on"])

computer_data = flag_data[flag_data['model_category'] == 'Computer']
plt.scatter(computer_data['cost'], (computer_data['warranty_expiration'] - computer_data['purchased_on']).dt.days / 365)
plt.xlabel('Cost ($)')
plt.ylabel('Warranty Period (Years)')
plt.title('Correlation between Cost and Warranty Period of Computers')
plt.show()
