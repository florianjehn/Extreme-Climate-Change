# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 09:34:55 2020

@author: Florian Jehn
"""
import pandas as pd
from scipy import interpolate
import numpy as np
from sklearn.metrics import auc

# Read in the extracted xy data from the weitzman curve
curve_xy = pd.read_csv("extracted_data.csv", sep=";")

# Interpolate it to make it more smooth
tck = interpolate.splrep(curve_xy["x"], curve_xy["y"],s=0)
# make someovershoot to not get artifacts around 0 and 10
x_new = np.arange(-5,15, 0.1)
y_new = interpolate.splev(x_new, tck, der=0)
curve_new = pd.DataFrame(data=[x_new, y_new]).transpose()
curve_new.columns=["x", "y"]
# cut it down to original size
curve_new = curve_new.iloc[50:151,:]
curve_new.reset_index(inplace=True, drop=True)
# Start is 0,0
curve_new.iloc[0,0] = 0
curve_new.iloc[0,1] = 0
# Calculat the different probabilities.
warming_prob = pd.DataFrame(index=range(1), columns = ["low", "inter", "high", "very high"])
warming_prob["low"] = auc(curve_new.loc[0:30,"x"], curve_new.loc[0:30, "y"])
warming_prob["inter"] = auc(curve_new.loc[30:50,"x"], curve_new.loc[30:50, "y"])
warming_prob["high"] = auc(curve_new.loc[50:70,"x"], curve_new.loc[50:70, "y"])
warming_prob["very high"] = auc(curve_new.loc[70:,"x"], curve_new.loc[70:, "y"])

warming_prob.transpose().to_csv("warming_probabilities.csv",sep=";")