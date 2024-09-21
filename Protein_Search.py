#!/usr/bin/env python3
#################################################
# Protein Search using ECOD's AlphaFold DataBase
# Creater: Luke Coster
##################################################
#This is the extra databases needed to be imported
import pandas as pd
import os
import matplotlib.pyplot as plt
###################################################
#!!! ADD YOUR INFORMATIOM HERE !!!
#--------------------------------------------------
#add the file path for your proteomic data (Excel Sheet)
your_data = ""

#Whar column is your uniprot IDs in (in python Column 1 = 0, Column 2 = 1 , ect.)
Uniprot_column = 0 #edit the number to your columns
#Would you like a pie chart summary of 
Pie_chart="yes"

###################################################

#This is opening the files for me adjust
human_alpha_fold_class = pd.read_excel("")

