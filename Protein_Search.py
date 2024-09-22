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
output_file = "[insert here].xlsx"

#Whar column is your uniprot IDs in (in python Column 1 = 0, Column 2 = 1 , ect.)
Uniprot_column = 0 #edit the number to your columns

#Would you like a pie chart summary of each subclass of domain structures (yes or no)
Pie_chart="" 
output_folder = "" #this is where the pie charts will go

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

#Finding your proteins Uniprot ID in Human Proteome Classifications
Your_data_with_ECOD_IDs_df = human_alpha_fold_class_df[human_alpha_fold_class_df.iloc[:,0].isin(your_data_onlyUniProt_df[:,0])]

#translating your proteins ECOD ID into domain names
#first need to make column names the same( to avoid errors )
ECOD_domain_dictionary_df = ECOD_domain_dictionary_df.rename(columns = {ECOD_domain_dictionary_df[0]: Your_data_with_ECOD_IDs_df[0]})
#now I can translate
Your_data_with_classifications_df = pd.merge(Your_data_with_ECOD_IDs_df, ECOD_domain_dictionary_df, on = Your_data_with_ECOD_IDs_df[0], how = 'inner')

###################################################

#Counting the proteins that were unclassified
Unclassified_proteins = total_protein - len(Your_data_with_classifications_df.columns[0])
print("There were " + Unclassified_proteins + " proteins classififed")

###################################################

# organizing data
# to create an organized excel sheet, we need to work with excel data not data frames
#create temporary files
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
with pd.ExcelFile(output_file, engine = "openpyxl") as writer:
    for sheet_name, df in new_sheet.items():
        df.to_excel(writer, sheet_name = sheet_name, index = False)

#removing temporary file
temporary_file = None
df = None
os.remove("temporary_file.xlsx")

print("Created organized sheet")

###################################################
#Creating Pie Charts
if Pie_chart == "yes":
    def create_pie_charts(output_file, output_folder):
        excel = pd.ExcelFile(output_file)

        if not os.path.exists(output_folder): #makes the folder
            os.makedirs(output_folder)

        count_arch = {}

        for sheet_name in excel.sheet_names:
            df = pd.read_excel(output_file, sheet_name = sheet_name)

            column_value = df.iloc[:,5]

            value_counts = column_value.value_counts()

        total_value_count = total_protein

        for sheet_name in xls.sheet_name:
            df = pd.read_excel(output_file, sheet_name = sheet_name)
print("Finished")
