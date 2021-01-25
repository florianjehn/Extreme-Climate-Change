# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 13:32:12 2020

@author: Florian Jehn
"""

import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
import calculate_probabilities as cp
from sklearn.metrics import auc


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
    ax.tick_params(axis=u'both', which=u'both',color="#676767")
    if with_legend:
      legend = ax.get_legend()
      for text in legend.get_texts():
        text.set_color("#676767")
      legend.get_title().set_color("#676767")
    ax.yaxis.get_offset_text().set_color("#676767")



def read_counts_total():
    # Read in the data
    ipcc_counts = pd.read_csv("Results" + os.sep + "temp_counts_all.csv", sep=";", index_col=0)
    
    # Replace the spaces in the temperature description
    ipcc_counts.index = ipcc_counts.index.str.replace(" ","")
    # Make temperatures numerical
    ipcc_counts.index = ipcc_counts.index.str.replace("°C","")
    ipcc_counts.reset_index(inplace=True)
    ipcc_counts.columns=["Temp Rise", "Count"]
    ipcc_counts["Temp Rise"] = ipcc_counts["Temp Rise"].astype(float)
    return ipcc_counts


def read_counts_1_5():
    # Read in the data
    counts_1_5_report = pd.read_csv("Results" + os.sep + "counts_SR15_Full_Report_High_Res.csv", sep=";", index_col=0)
    # Replace the spaces in the temperature description
    counts_1_5_report.index = counts_1_5_report.index.str.replace(" ","")
    # Make temperatures numerical
    counts_1_5_report.index = counts_1_5_report.index.str.replace("°C","")
    counts_1_5_report.reset_index(inplace=True)
    counts_1_5_report.columns=["Temp Rise", "Count"]
    counts_1_5_report["Temp Rise"] = counts_1_5_report["Temp Rise"].astype(float)
    return counts_1_5_report


def read_probability_curves(ppm):
    prob_temp = pd.read_csv("Data" + os.sep + "wagner_weitzman_2015_"+ str(ppm)+"ppm.csv", sep=";", index_col=0)
    return prob_temp


def prepare_data_a():  
    total_counts = read_counts_total()
    curve_550 = cp.interpolate_curve(cp.read_data(550))
    curve_700 = cp.interpolate_curve(cp.read_data(700))
    return total_counts, curve_550, curve_700


def prepare_data_b():
    total_counts = read_counts_total()
    counts_1_5 = read_counts_1_5()
    without_1_5 = pd.DataFrame(total_counts[total_counts.columns[-1]] - counts_1_5[counts_1_5.columns[-1]])
    without_1_5["Temp Rise"] = total_counts["Temp Rise"]  
    without_1_5.columns = ["Count", "Temp Rise"]
    curve_550 = cp.interpolate_curve(cp.read_data(550))
    curve_700 = cp.interpolate_curve(cp.read_data(700))    
    return without_1_5, curve_550, curve_700


def prepare_data_c():
    total_counts = read_counts_total()
    total = total_counts.sum()
    # Convert counts to percent
    total_counts_percent = (total_counts / total) * 100
    count_over_3 = pd.DataFrame(total_counts_percent.iloc[5:].sum()).transpose()
    
    # Get the probability of the values above 3°C
    curve_700 = cp.interpolate_curve(cp.read_data(700))    
    prob_over_3 = auc(curve_700.loc[300:,"x"], curve_700.loc[300:, "y"])
    
    return count_over_3.loc[0,"Count"], prob_over_3
    


def prepare_data_d():
    total_counts = read_counts_total()
    total = total_counts.sum()
    # Convert counts to percent
    total_counts_percent = (total_counts / total) * 100
    count_over_6 = pd.DataFrame(total_counts_percent.iloc[11:].sum()).transpose()
    
    # Get the probability of the values above 3°C
    curve_700 = cp.interpolate_curve(cp.read_data(700))    
    prob_over_6 = auc(curve_700.loc[600:,"x"], curve_700.loc[600:, "y"])
    
    return count_over_6.loc[0,"Count"], prob_over_6

def create_grid():  
    """Plots the main figures for the different ppm"""  
    # Create a gridspec to plot in
    fig = plt.figure()
    gs = fig.add_gridspec(2,4,wspace=1.1,hspace=0.5)
    ax1 = fig.add_subplot(gs[0,:])
    ax2 = fig.add_subplot(gs[1,:2])
    ax3 = fig.add_subplot(gs[1,2])
    ax4 = fig.add_subplot(gs[1,3])
    axes = [ax1, ax2, ax3, ax4]
    return axes


def plot_figure(color_prob, color_count, edgecolor):
    axes = create_grid()
    
    # Get data for fig a)
    total_counts, curve_550, curve_700 = prepare_data_a()
    # Plot fig a)
    axes[0].bar(x=total_counts["Temp Rise"],height=total_counts["Count"], width=0.3,color=color_count,label="Occurence in IPCC reports")
    axes.append(axes[0].twinx())
    axes[4].plot(curve_550["x"], curve_550["y"], color=color_prob, linestyle="--", label="Probability curve for 550 ppm")
    axes[4].plot(curve_700["x"], curve_700["y"], color=color_prob, label="Probability curve for 700 ppm")
    axes[4].set_xlim(-0.5,10.5)
    axes[4].set_ylim(0,0.4)
    axes[4].bar(2,0,color=color_count,label="Occurence in IPCC reports")
    legend = plt.legend()
    # make legend nicer
    for text in legend.get_texts():
        text.set_color("#676767")
    
    # Get data for fig b)
    without_1_5, curve_550, curve_700 = prepare_data_b()
    axes[1].bar(x=without_1_5["Temp Rise"],height=without_1_5["Count"], width=0.3,color=color_count)
    axes.append(axes[1].twinx())
    axes[5].plot(curve_550["x"], curve_550["y"], color=color_prob, linestyle="--", label="550 ppm")
    axes[5].plot(curve_700["x"], curve_700["y"], color=color_prob, label="700 ppm")
    axes[5].set_xlim(-0.5,10.5)
    axes[5].set_ylim(0,0.4)
    
    # Get data for fig c)
    count_over_3, prob_over_3 = prepare_data_c()
    axes[2].bar(x=1.5,height=count_over_3,width=0.04, color=color_count)
    axes.append(axes[2].twinx())
    axes[6].bar(x=1.6,height=prob_over_3,width=0.04, color=color_prob)
    axes[2].set_ylim(0,65)
    axes[6].set_ylim(0,0.65)
    axes[2].set_xlim(1.35, 1.75)
    axes[2].set_xticklabels([""])

    
    # Get data for fig d)
    count_over_6, prob_over_6 = prepare_data_d()
    axes[3].bar(x=1.5,height=count_over_6,width=0.04, color=color_count)
    axes.append(axes[3].twinx())
    axes[7].bar(x=1.6,height=prob_over_6,width=0.04, color=color_prob)
    axes[3].set_ylim(0,65)
    axes[7].set_ylim(0,0.65)
    axes[3].set_xlim(1.35, 1.75)
    axes[3].set_xticklabels([""])
    
    # Set lables
    for ax in [axes[0], axes[1]]:
        ax.set_ylabel("Absolute Occurence [/]")
        ax.set_xlabel("Temperature Change [°C]")
        ax.locator_params(axis='x', nbins=20)
    
    for ax in [axes[2],axes[3]]:
        ax.set_ylabel("Relative Occurence [%]")

    for ax in axes[4:]:
        ax.set_ylabel("Warming Probability [/]")
    
    axes[0].set_title("a) Temperature count in AR5 working group reports and special reports until 2020")
    axes[1].set_title("b) Excluding special report on 1.5°C warming")
    axes[2].set_title("c) 3°C and above")
    axes[3].set_title("d) 6°C and above")
    
    
    
    # make nicer
    i = 0
    for ax in axes:
        plot_nicer(ax, with_legend=False)
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=0)
    
    for ax in [axes[2], axes[3], axes[6], axes[7]]:
        ax.tick_params(axis="x", which=u'both',length=0)

    fig=plt.gcf()
    fig.set_size_inches(12,6)
    fig.tight_layout()
    plt.savefig("Figures" + os.sep + "warming_curves.png",dpi=200, bbox_inches="tight")
    plt.close()
    
if __name__ == "__main__":
    # Read the data
    color_prob = "#3A3A3A"
    color_count = "#BD7F37FF"
    edgecolor = "white"

    plot_figure(color_prob, color_count, edgecolor)
        
    
    
    
    
    

