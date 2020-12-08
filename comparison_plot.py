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
    spine.set_color("lightgray")
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
counts_1_5_report = pd.read_csv("temp_counts_1_5_special_report.csv", sep=";",index_col=0)

# Create a gridspec to plot in
fig = plt.figure()
gs = fig.add_gridspec(2,4)
ax1 = fig.add_subplot(gs[0,:])
ax2 = fig.add_subplot(gs[1,:2])
ax3 = fig.add_subplot(gs[1,2])
ax4 = fig.add_subplot(gs[1,3])

# Replace the spaces in the temperature description
ipcc_counts.index = ipcc_counts.index.str.replace(" ","")
counts_1_5_report.index = counts_1_5_report.index.str.replace(" ","")

# Convert probability to percent
prob_temp = prob_temp * 100

##### Preparation for the count without 1_5 report
without_1_5 = ipcc_counts - counts_1_5_report
without_1_5_total = without_1_5.sum()
# Convert to percent
without_1_5[without_1_5.columns[0]] = (without_1_5/without_1_5_total) * 100
# merge
compare_df_without_1_5 = without_1_5.merge(prob_temp,left_index=True, right_index=True)
compare_df_without_1_5.columns = ["Relative Occurence in IPCC Reports", "Probability of Warming"]


##### Preparation for the total counts
ipcc_total = ipcc_counts.sum()
# Convert counts to percent
ipcc_counts[ipcc_counts.columns[0]] = (ipcc_counts / ipcc_total) * 100
# merge
compare_df = ipcc_counts.merge(prob_temp,left_index=True, right_index=True)
compare_df.columns = ["Relative Occurence in IPCC Reports", "Probability of Warming"]




##### Preparation for the >=6°C and >=3°C Plot
# Only use the values for 6 and above
over_6 = pd.DataFrame(compare_df.iloc[11:].sum()).transpose()
# The sum of probability is slightly above 10 because of the way it is 
# calculated from the pdf. Set to 10 here, so it is in line with Wagner and 
# Weitzmann
over_6.iloc[0,1] = 10
over_3 = pd.DataFrame(compare_df.iloc[5:].sum()).transpose()


##### Plot the total count
compare_df.plot(kind="bar", ax=ax1,zorder=5)
ax1.set_title("a) Temperature Count In All Major IPCC Reports Since AR5")


#### Plot without the 1.5 special report
compare_df_without_1_5.plot(kind="bar", ax=ax2, legend=False,zorder=5)
ax2.set_title("b) Excluding Special Report On 1.5°C Warming")
plt.setp(ax2.xaxis.get_majorticklabels(), fontsize=6)


#### Plot 3
over_3.plot(kind="bar", ax=ax3, width=0.1, legend=False,zorder=5)
ax3.set_title("c) 3°C And Above")
plt.setp(ax3.xaxis.get_majorticklabels(), color="white")


#### Plot only 6 degrees and above
over_6.plot(kind="bar", ax=ax4, width=0.1, legend=False,zorder=5)
ax4.set_title("d) 6°C And Above")
plt.setp(ax4.xaxis.get_majorticklabels(), color="white")



# # make nicer
i = 0
for ax in [ax1, ax2, ax3, ax4]:
    ax.set_ylabel("Percentage [%]")
    if i == 0:
        plot_nicer(ax)
    else: 
        plot_nicer(ax, with_legend=False)
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=0)
    i +=1

fig=plt.gcf()
fig.set_size_inches(12,6)
fig.tight_layout()
plt.savefig("warming_count.png",dpi=200, bbox_inches="tight")

