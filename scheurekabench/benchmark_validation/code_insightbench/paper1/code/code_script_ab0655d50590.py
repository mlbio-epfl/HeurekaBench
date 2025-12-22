import os
import json
import argparse
import requests
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pandas import date_range
plt.figure(figsize=(10, 6))
boxplot = sns.boxplot(x='contains_keywords', y='target_percentage', data=df, showmeans=True,
                      meanprops={"marker":"o", "markerfacecolor":"red", "markersize":"10"},
                    #   medianprops={"color": "blue", "linewidth": 2},
                      whiskerprops={"linewidth": 2},
                      capprops={"linewidth": 2})

# Annotate the boxplot with the mean and median values
for i in range(2):
    group_data = df[df['contains_keywords'] == i]['target_percentage']
    mean_val = group_data.mean()
    median_val = group_data.median()

    plt.text(i, mean_val, f'{mean_val:.2f}', color='red', ha='center', va='bottom')
    # plt.text(i, median_val, f'{median_val:.2f}', color='blue', ha='center', va='bottom')

plt.title('Target Percentage by Presence of Keywords in Description')
plt.xlabel('Contains Keywords')
plt.ylabel('Target Percentage')
plt.xticks([0, 1], ['No Keywords', 'Has Keywords'])
plt.grid(True, axis='y', linestyle='--', alpha=0.7)
plt.show()
