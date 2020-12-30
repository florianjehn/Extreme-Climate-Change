# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 13:32:12 2020

@author: Florian Jehn
"""

import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np


def plot_nicer(ax, with_legend=True):
  """Takes an axis objects and makes it look nicer"""
  alpha=0.7
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


def read_counts():
    # Read in the data
    ipcc_counts = pd.read_csv("Results" + os.sep + "temp_counts_all.csv", sep=";", index_col=0)
    counts_1_5_report = pd.read_csv("Results" + os.sep + "counts_SR15_Full_Report_High_Res.csv", sep=";",index_col=0)
    
    # Replace the spaces in the temperature description
    ipcc_counts.index = ipcc_counts.index.str.replace(" ","")
    counts_1_5_report.index = counts_1_5_report.index.str.replace(" ","")
    return ipcc_counts, counts_1_5_report


def read_probability(ppm):
    prob_temp = pd.read_csv("Results" + os.sep + "warming_probabilities_"+ str(ppm)+"ppm.csv", sep=";", index_col=0)
    return prob_temp


def prepare_warming_data():
    """
    Reads in all the warming probabilities and combines them into one dataframe
    """
    warming_df = pd.DataFrame()
    for ppm in np.arange(400, 1001, 50):
        prob_temp = read_probability(ppm)
        # Convert probability to percent
        prob_temp = prob_temp * 100
        warming_df = pd.concat([warming_df, prob_temp])


def prepare_count_data(ipcc_counts):
    
    
    ##### Preparation for the count without 1_5 report
    without_1_5 = pd.DataFrame(ipcc_counts[ipcc_counts.columns[0]] - 
                               counts_1_5_report[counts_1_5_report.columns[0]])
    without_1_5_total = without_1_5.sum()
    # Convert to percent
    without_1_5[without_1_5.columns[0]] = (without_1_5/without_1_5_total) * 100
    # merge
    compare_df_without_1_5 = without_1_5.merge(prob_temp,left_index=True, right_index=True)
    compare_df_without_1_5.columns = ["Relative occurence in IPCC reports", "Probability of warming"]
    
    
    ##### Preparation for the total counts
    ipcc_total = ipcc_counts.sum()
    # Convert counts to percent
    ipcc_counts_percent = (ipcc_counts / ipcc_total) * 100
    # merge
    compare_df = ipcc_counts_percent.merge(prob_temp,left_index=True, right_index=True)
    compare_df.columns = ["Relative occurence in IPCC reports", "Probability of warming"]
    
    ##### Preparation for the >=6°C and >=3°C Plot
    over_6 = pd.DataFrame(compare_df.iloc[11:].sum()).transpose()
    over_3 = pd.DataFrame(compare_df.iloc[5:].sum()).transpose()
    
    return compare_df, compare_df_without_1_5, over_3, over_6


def plot_figures(compare_df, compare_df_without_1_5, over_3, over_6, ppm, 
                 color_prob, color_count, edgecolor):  
    """Plots the main figures for the different ppm"""  

    fig=plt.gcf()
    fig.set_size_inches(12,6)
    fig.tight_layout()
    plt.savefig("Figures" + os.sep + "warming_count_"+str(ppm)+".png",dpi=200, bbox_inches="tight")
    plt.close()
    
if __name__ == "__main__":
    # Read the data
    ipcc_counts, counts_1_5_report = read_counts()
    color_prob = "#BD7F37FF"
    color_count = "#A13941FF"
    edgecolor = "white"
    # Run for all ppm
    for ppm in np.arange(400, 1001, 50):
        prob_temp = read_probability(ppm)
        compare_df, compare_df_without_1_5, over_3, over_6 = prepare_data(
            prob_temp, ipcc_counts, counts_1_5_report)
        plot_figures(compare_df, compare_df_without_1_5, over_3, over_6, ppm, 
                     color_prob, color_count, edgecolor)
        
    
    
    
    
    

