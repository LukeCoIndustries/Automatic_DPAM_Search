#!/usr/bin/env python3
#################################################
# Protein Search using ECOD's AlphaFold DataBase
# Creater: Luke Coster
##################################################
#This is the extra databases needed to be imported
import pandas as pd
import os
import matplotlib.pyplot as plt

# make sure you have pandas and matplotlib downloaded
# if not type "pip intall pandas" and "pip install matplotlib" in your command terminal
###################################################
#!!! ADD YOUR INFORMATIOM HERE !!!
#--------------------------------------------------
#add the relative path to your proteomic data file (Excel Sheet)
your_data = ""

#What do you want you output file to be named (replace [insert here])
output_file = ""+".xlsx"

#Whar column is your uniprot IDs in (in python Column 1 = 0, Column 2 = 1 , ect.)
Uniprot_column = 0 #edit the number to your columns

# What column is your Z score (in python Column 1 = 0, Column 2 = 1 , ect.)
Z_score_column = 0 #change to your column

#How many proteins do you want to lookn at (starts at the top Z score)
number_of_proteins = 0

#Do you want each arch name (all alpha,all beta, alpha superhelix, ect) to be organized into their own sheet
organize = "" #yes or no (please type in all lowercase)

###################################################

print("started")
#This is opening the files for me adjust
human_alpha_fold_class_raw_df = pd.read_excel("HomSa_raw_domains.xlsx") #Contains Uniprot ID's And ECOD domain classifications for AlphaFold Models
ECOD_domain_dictionary_raw_df = pd.read_excel("ecod.latest.domains.xlsx") #ECOD domain classification ID  Dictionary (contains duplicates and redundancies)(version 1.6)
your_data_df = pd.read_excel(your_data)
print("loaded files")

#this takes your file and ranks it highest to lowest z scores
your_data_sort_df= your_data_df.sort_values(by=your_data_df.columns[Z_score_column], ascending=False)
your_data_only_top_number_df = your_data_sort_df.head(number_of_proteins)
print(your_data_only_top_number_df)
your_data_sort_df.to_excel("test.xlsx", index = False)
###################################################

#Cleaning redundancies and duplicates or data that is not needed
ECOD_domain_dictionary_df = ECOD_domain_dictionary_raw_df.drop(ECOD_domain_dictionary_raw_df.columns[[0,1,2,4,5,6,7,8,13,14,15]], axis = 1)
ECOD_domain_dictionary_df.drop_duplicates(inplace = True)
human_alpha_fold_class_df = human_alpha_fold_class_raw_df.drop(human_alpha_fold_class_raw_df.columns[[1,2,4,5]], axis = 1)
human_alpha_fold_class_df.drop_duplicates(inplace= True)

print("cleaned redundancies")

###################################################

#Counts how many proteins we have at the start
total_protein = len(your_data_only_top_number_df)
print("There are "+str(total_protein)+" proteins")

###################################################

#Finding your proteins Uniprot ID in Human Proteome Classifications
Your_data_with_ECOD_IDs_df = human_alpha_fold_class_df[human_alpha_fold_class_df.iloc[:,0].isin(your_data_only_top_number_df.iloc[:,Uniprot_column])]

#translating your proteins ECOD ID into domain names
#first need to make column names the same( to avoid errors )
ECOD_domain_dictionary_df = ECOD_domain_dictionary_df.rename(columns = {ECOD_domain_dictionary_df.columns[0]: Your_data_with_ECOD_IDs_df.columns[1]})
#now I can translate
Your_data_with_classifications_df = pd.merge(Your_data_with_ECOD_IDs_df, ECOD_domain_dictionary_df, on = Your_data_with_ECOD_IDs_df.columns[1], how = 'inner')

#This is giving names to each column
Your_data_with_classifications_df.rename(columns={Your_data_with_classifications_df.columns[0]:'UniProt', Your_data_with_classifications_df.columns[1]: 'ECOD T-group identifier', Your_data_with_classifications_df.columns[2]:'arch_name', Your_data_with_classifications_df.columns[3]: 'x_name', Your_data_with_classifications_df.columns[4]: 'h_name', Your_data_with_classifications_df.columns[5]: 't_name'}, inplace = True)

###################################################

#making an area for proteins that were not classified by ECOD
for value in your_data_only_top_number_df[your_data_only_top_number_df.columns[Uniprot_column]].values:
    if value not in Your_data_with_classifications_df['UniProt'].values:
        newrow = {'UniProt': value, 'ECOD T-group identifier': 'no found', 'arch_name': "undefined", 'x_name': "undefined", 'h_name': "undefined", "t_name": "undefined"}
        Your_data_with_classifications_df.loc[len(Your_data_with_classifications_df)]= newrow
    
#

###################################################

# organizing data
# to create an organized excel sheet, we need to work with excel data not data frames
#create temporary files
if organize == 'yes':
    Your_data_with_classifications_df.to_excel("temporary_file.xlsx", index = False)
    temporary_file = pd.ExcelFile("temporary_file.xlsx")

    #replacing / with _ in the ECOD Names
    def replace_slash(value):
        return value.replace('/','_')

    #creating an empty dictionary for future sheet creation
    new_sheet = {}

    #Organizng
    for sheet_name in temporary_file.sheet_names:
        df = temporary_file.parse(sheet_name)
        df['arch_name'] = df["arch_name"].apply(replace_slash)
        arch_name = df.iloc[:,2]
        for value in arch_name.unique():
            if pd.notna(value):
                if value not in arch_name:
                    new_sheet[value] = pd.DataFrame(columns=df.columns)
                add_row = df[arch_name == value]
                new_sheet[value] = pd.concat([new_sheet[value], add_row])

    #Creating the excel
    with pd.ExcelWriter(output_file, engine = "openpyxl") as writer:
        for sheet_name, df in new_sheet.items():
            df.to_excel(writer, sheet_name = sheet_name, index = False)
    os.remove("temporary_file.xlsx")
elif organize == 'no':
    Your_data_with_classifications_df.to_excel(output_file, index =False)
else:
    print("you did not say you wanted it organized or not")
