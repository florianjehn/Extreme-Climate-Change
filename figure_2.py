# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 13:32:12 2020

@author: Florian Jehn
"""

import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
import seaborn as sns


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
        prob_temp = round(prob_temp * 100,0)
        warming_df = pd.concat([warming_df, prob_temp],axis=1)
    warming_df.columns = [str(i) + " ppm" for i in np.arange(400, 1001,50)]
    warming_df = warming_df.transpose()
    return warming_df


def prepare_count_data():
    """
    Reads in the counts of the ipcc and changes them to percent
    """    
    # Read in the data
    ipcc_counts = pd.read_csv("Results" + os.sep + "temp_counts_all.csv", sep=";", index_col=0)
    # Replace the spaces in the temperature description
    ipcc_counts.index = ipcc_counts.index.str.replace(" ","")
    ##### Preparation for the total counts
    ipcc_total = ipcc_counts.sum()
    # Convert counts to percent
    ipcc_counts_percent = round((ipcc_counts / ipcc_total) * 100,0)
    
    return ipcc_counts_percent


def plot_figure(combine_df):  
    """Plots the main figures for the different ppm"""  
    ax = sns.heatmap(combine_df,cmap="OrRd", linewidth=0.2, square=True, annot=True, cbar=False)
    # Add a line to mark the counts
    ax.hlines([13], *ax.get_xlim())
    fig=plt.gcf()
    fig.set_size_inches(12,6)
    fig.tight_layout()
    plt.savefig("Figures" + os.sep +"heatmap.png",dpi=200, bbox_inches="tight")
    
if __name__ == "__main__":
    # Read the data
    ipcc_counts = prepare_count_data()
    ipcc_counts.columns = ["IPCC Counts"]
    warming_df = prepare_warming_data()
    combine_df = pd.concat([warming_df, ipcc_counts.transpose()])
    plot_figure(combine_df)


    
    
    
    
    

