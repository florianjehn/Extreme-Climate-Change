# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 13:32:12 2020

@author: Florian Jehn
"""

import pandas as pd
import matplotlib.pyplot as plt

def plot_nicer(ax, with_legend=True):
  """Takes an axis objects and makes it look nicer"""
  alpha=0.7
  # Remove borders
  for spine in ax.spines.values():
    spine.set_visible(False)
  # Make text grey
  plt.setp(ax.get_yticklabels(), alpha=alpha)
  plt.setp(ax.get_xticklabels(), alpha=alpha)
  ax.set_xlabel(ax.get_xlabel(), alpha=alpha)
  ax.set_ylabel(ax.get_ylabel(), alpha=alpha)
  ax.set_title(ax.get_title(), alpha=alpha)
  ax.tick_params(axis=u'both', which=u'both',length=0)
  if with_legend:
    legend = ax.get_legend()
    for text in legend.get_texts():
      text.set_color("#676767")
    legend.get_title().set_color("#676767")
  ax.yaxis.get_offset_text().set_color("#676767")
  # Add a grid
  ax.yaxis.grid(True, color="lightgrey", zorder=0)
  ax.xaxis.grid(False)

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
compare_df.columns = ["Relative Occurence in IPCC Reports", "Probability of Warming"]
# compare_df["Temperature"] = compare_df.index
# compare_df.reset_index(inplace=True, drop=True)

# plot
ax= compare_df.plot(kind="bar")
# make nicer
ax.set_ylabel("Percentage [%]")
plot_nicer(ax)
plt.xticks(rotation=0)

fig=plt.gcf()
fig.set_size_inches(8,4)
fig.tight_layout()
plt.savefig("warming_count.png",dpi=200, bbox_inches="tight")

