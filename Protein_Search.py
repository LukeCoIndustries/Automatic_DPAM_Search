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
#Would you like a pie chart summary of each subclass of domain structures (yes or no)
Pie_chart="" 

###################################################

#This is opening the files for me adjust
human_alpha_fold_class_raw_df = pd.read_excel("HomSa_raw_domains.xlsx") #Contains Uniprot ID's And ECOD domain classifications for AlphaFold Models
ECOD_domain_dictionary_raw_df = pd.read_excel("ecod.latest.domains.xlsx") #ECOD domain classification ID Dictionary (contains duplicates and redundancies)
your_data_df = pd.read_excel(your_data)

###################################################

#Cleaning redundancies and duplicates or data that is not needed
ECOD_domain_dictionary_df = ECOD_domain_dictionary_raw_df.drop(ECOD_domain_dictionary_raw_df.columns[0,1,2,4,5,6,7,8,13,14,15], axis = 1)
ECOD_domain_dictionary_df.drop_duplicates(inplace = True)
human_alpha_fold_class_df = human_alpha_fold_class_raw_df.drop(human_alpha_fold_class_raw_df.columns[1,2,4,5], axis = 1)
human_alpha_fold_class_df.drop_duplicates(inplace= True)
your_data_onlyUniProt_df = your_data_df.columns[Uniprot_column]

###################################################

#Counts how many proteins we have at the start
total_protein = len(your_data_onlyUniProt_df)
print("There are "+total_protein+" proteins")

###################################################



