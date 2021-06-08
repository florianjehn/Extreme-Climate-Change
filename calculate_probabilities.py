# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 09:34:55 2020

@author: Florian Jehn
"""
import pandas as pd
from scipy import interpolate
import numpy as np
from sklearn.metrics import auc
import os


def read_data(ppm):
    # Read in the extracted xy data from the weitzman curve
    curve_xy = pd.read_csv("Data" + os.sep + "wagner_weitzman_2015_"+str(ppm)+"ppm.csv", sep=";")
    return curve_xy


def interpolate_curve(curve_xy):
    # Interpolate it to make it more finely grained
    tck = interpolate.splrep(curve_xy["x"], curve_xy["y"],s=0)
    # make someovershoot to not get artifacts around 0 and 10
    x_new = np.arange(-2,12, 0.01)
    y_new = interpolate.splev(x_new, tck, der=0)
    curve_new = pd.DataFrame(data=[x_new, y_new]).transpose()
    curve_new.columns=["x", "y"]
    # cut it down to original size
    curve_new = curve_new.iloc[200:1301,:]
    curve_new.reset_index(inplace=True, drop=True)
    # Start is 0,0
    curve_new.iloc[0,0] = 0
    curve_new.iloc[0,1] = 0
    # Return
    return curve_new


def get_probability(curve_new, ppm):
    # Calculat the different probabilities.
    warming_prob = pd.DataFrame(index=[0])
    # by temperature .5°C
    warming_prob["0.5°C"] = auc(curve_new.loc[25:75,"x"], curve_new.loc[25:75, "y"])
    warming_prob["1°C"] = auc(curve_new.loc[75:125,"x"], curve_new.loc[75:125, "y"])
    warming_prob["1.5°C"] = auc(curve_new.loc[125:175,"x"], curve_new.loc[125:175, "y"])
    warming_prob["2°C"] = auc(curve_new.loc[175:225,"x"], curve_new.loc[175:225, "y"])
    warming_prob["2.5°C"] = auc(curve_new.loc[225:275,"x"], curve_new.loc[225:275, "y"])
    warming_prob["3°C"] = auc(curve_new.loc[275:325,"x"], curve_new.loc[275:325, "y"])
    warming_prob["3.5°C"] = auc(curve_new.loc[325:375,"x"], curve_new.loc[325:375, "y"])
    warming_prob["4°C"] = auc(curve_new.loc[375:425,"x"], curve_new.loc[375:425, "y"])
    warming_prob["4.5°C"] = auc(curve_new.loc[425:475,"x"], curve_new.loc[425:475, "y"])
    warming_prob["5°C"] = auc(curve_new.loc[475:525,"x"], curve_new.loc[475:525, "y"])
    warming_prob["5.5°C"] = auc(curve_new.loc[525:575,"x"], curve_new.loc[525:575, "y"])
    warming_prob["6°C"] = auc(curve_new.loc[575:625,"x"], curve_new.loc[575:625, "y"])
    warming_prob["6.5°C"] = auc(curve_new.loc[625:675,"x"], curve_new.loc[625:675, "y"])
    warming_prob["7°C"] = auc(curve_new.loc[675:725,"x"], curve_new.loc[675:725, "y"])
    warming_prob["7.5°C"] = auc(curve_new.loc[725:775,"x"], curve_new.loc[725:775, "y"])
    warming_prob["8°C"] = auc(curve_new.loc[775:825,"x"], curve_new.loc[775:825, "y"])
    warming_prob["8.5°C"] = auc(curve_new.loc[825:875,"x"], curve_new.loc[825:875, "y"])
    warming_prob["9°C"] = auc(curve_new.loc[875:925,"x"], curve_new.loc[875:925, "y"])
    warming_prob["9.5°C"] = auc(curve_new.loc[925:975,"x"], curve_new.loc[925:975, "y"])
    warming_prob["10°C"] = auc(curve_new.loc[975:1025,"x"], curve_new.loc[975:1025, "y"])
    # Save    
    warming_prob.transpose().to_csv("Results" +os.sep+ "warming_probabilities_"+str(ppm)+"ppm.csv",sep=";")


if __name__ == "__main__":
    # Run for all ppm
    for ppm in np.arange(400, 1001, 50):
        curve_xy = read_data(ppm)
        curve_new = interpolate_curve(curve_xy)
        get_probability(curve_new, ppm)       