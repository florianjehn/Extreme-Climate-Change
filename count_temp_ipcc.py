# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 11:56:42 2020

@author: Florian Jehn
"""
import re
import numpy as np
import pandas as pd


from pdfminer3.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer3.converter import TextConverter
from pdfminer3.layout import LAParams
from pdfminer3.pdfpage import PDFPage
from io import StringIO

def convert_pdf_to_txt(path):
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
            print("Finished the all pages until page " + str(i))
        interpreter.process_page(page)
        i += 1

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text

# Working Group Reports
# Donadloadable at https://www.ipcc.ch/working-groups/
wg1 = "WG1AR5_all_final.pdf"
wg2 = "WGIIAR5-PartA_FINAL.pdf"
wg3 = "ipcc_wg3_ar5_full.pdf"

# Count all the temperatere
temp_dict = {}
for i in np.arange(0.5,10.5, 0.5):
    # Test if it is a float or not to format it right
    if i == int(i):
        # Add an empty space at the beginnign to make sure this is not just counting the 1.5°C and so forth as 5°C
        key = " " + str(int(i)) + "°C"
    else: 
        key = " " + str(i )+ "°C"
    temp_dict[key] = 0
        
# Go through all working group reports
for wg in [wg1, wg2, wg3]:
    print("Starting with " + wg)
    # Read it in 
    text = convert_pdf_to_txt(wg)
    # count how often a temperature occures
    for temp in temp_dict.keys():
        number_of_occurences = len(re.findall(temp, text))   
        if number_of_occurences > 0: 
            print("Found " + temp +  " " + str(number_of_occurences) + " time(s)")
            temp_dict[temp] += number_of_occurences

            
# Save the results
temp_counts = pd.DataFrame.from_dict(temp_dict, orient="index")
temp_counts.to_csv("temp_counts.csv", sep=";")