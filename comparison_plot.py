# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 13:32:12 2020

@author: Florian Jehn
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Read in the data
prob_temp = pd.read_csv("warming_probabilities.csv", sep=";", index_col=0)
ipcc_counts = pd.read_csv("temp_counts.csv", sep=";", index_col=0)
# Replace the spaces
ipcc_counts.index = ipcc_counts.index.str.replace(" ","")
# Convert counts to percent
ipcc_total = ipcc_counts.sum()
ipcc_counts[ipcc_counts.columns[0]] = (ipcc_counts / ipcc_total) * 100

# Convert probability to percent
prob_temp = prob_temp * 100

# merge
compare_df = ipcc_counts.merge(prob_temp,left_index=True, right_index=True)
compare_df.columns = ["Occurence in IPCC", "Probability of Warming"]
compare_df["Temperature"] = compare_df.index
compare_df.reset_index(inplace=True, drop=True)

# plot
#tidy_df = compare_df.melt(id_vars="Temperature")
sns.barplot(data=compare_df, order="Temperature")

# Make it nice
sns.set_style("whitegrid")
sns.despine(left=True)
