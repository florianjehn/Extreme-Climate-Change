# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 11:56:42 2020

@author: Florian Jehn
"""
import re
import numpy as np
import pandas as pd
import os

from pdfminer3.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer3.converter import TextConverter
from pdfminer3.layout import LAParams
from pdfminer3.pdfpage import PDFPage
from io import StringIO

def convert_pdf_to_txt(path):
    """
    Takes a path and reads the pdf there. Scraps all the text and returns 
    it as one big string. 
    """
    # Method taken from https://stackoverflow.com/questions/26494211/extracting-text-from-a-pdf-file-using-pdfminer-in-python
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()
    i = 0
    print("Starting to read in the single pages")
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        # Give some feedback that somethign is happening
        if i % 50 == 0:
            print("Finished all pages until page " + str(i))
        interpreter.process_page(page)
        i += 1

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text


def create_temp_dict():
    """Creates a dictionary for all the single temperatures to count and returns it"""
    temp_dict = {}
    for i in np.arange(0.5,10.5, 0.5):
        # Test if it is a float or not to format it right
        if i == int(i):
            # Add an empty space at the beginnign to make sure this is not counting e.g. 1.5°C  as 5°C
            key = " " + str(int(i)) + "°C"
        else: 
            key = " " + str(i )+ "°C"
        temp_dict[key] = 0
    return temp_dict
    
    

# Working Group Reports
# Downloadable at https://www.ipcc.ch/working-groups/
cwd = os.getcwd()
reports = [file for file in os.listdir(cwd + os.sep + "reports") if file[-4:] == ".pdf" ]

temp_counts = pd.DataFrame()
# Go through all working group reports
for report in reports:
    print("Starting with " + report)
    # Read it in 
    text = convert_pdf_to_txt("reports" + os.sep + report)
    temp_dict = create_temp_dict()
    # count how often a temperature occures
    for temp in temp_dict.keys():
        number_of_occurences = len(re.findall(temp, text))   
        if number_of_occurences > 0: 
            print("Found " + temp +  " " + str(number_of_occurences) + " time(s)")
            temp_dict[temp] += number_of_occurences
    # Save the results for the single pdf
    temp_counts_pdf = pd.DataFrame.from_dict(temp_dict, orient="index")
    temp_counts_pdf.to_csv("Results" + os.sep + "counts_" + report[:-4] + ".csv", sep=";")
    # Combine it with the overall data
    temp_counts = pd.concat([temp_counts, temp_counts_pdf],axis=1)
    
            
# Save the results
temp_counts = temp_counts.sum(axis=1)
temp_counts.to_csv("Results" + os.sep + "temp_counts_all.csv", sep=";")