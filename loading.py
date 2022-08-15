import glob
from time import time
import pandas as pd
import liquepy as lq
import matplotlib.pyplot as plt
from filepaths import *
import datetime


def load_dataframe(out_fp):
    """"
    Iterates through the output folder, looking for all csv and 
    converts them to a data frame appending them row by row.
    It holds the following data:
    :param out_fp: str
        Folder path of existing  CPT files in CSV format
    :param save_fp: str
        Folder path where dataframe files should be saved
    """
    ffps = glob.glob(out_fp + "*.csv") #

    headers = ['Date:', 'Assumed GWL:', 'groundlvl','Pre-Drill:', 'Easting', 'Northing',
                'aratio','CPT-ID','Object']
    hh = headers[0:-2]
    dfo = pd.DataFrame(columns = [""]*9)
    dfo.columns = headers
    for i,file in enumerate(ffps):
        #print(file)
        name = file.split('CPT_')[-1].split('.csv')[0]
        df = pd.read_csv(file, sep = ';')
        limit = 24
        new_df = df.iloc[:limit,0:2]

        #Create a list out of the dataframe rows, and search for the corresponding values
        series1=list(new_df.iloc[:,0])
        series2=list(new_df.iloc[:,1])
        dicty = dict(zip(series1,series2))

        l=[] #Initiate empty list to store the dict values based on the order of appeareance 
        for x in hh:
            l.append(dicty[x])

        vals = dict(zip(headers,l))
        #print(vals)
        cpt = lq.field.load_mpa_cpt_file(file, delimiter=";")
        #Create a list out of the dictionary values
        val_list = list(vals.values())
        val_list.extend([name,cpt]) #Grow list to the size of headers
        #Append to data frame
        dfo.loc[i,:] = val_list

    return dfo


def save_df_to_excel(df, name = "00_Header&Data.xlsx"):
    """ 
    Save a dataframe to excel

    """
    excel_file = pd.ExcelWriter("00_Header&Data.xlsx")
    df.to_excel(excel_file, sheet_name = 'df')
    excel_file.save()

    return None

def convert_to_dtype(df):
    """
    

    """
    df['groundlvl'] = df['groundlvl'].astype(float)
    df['Date:'] = pd.to_datetime(df['Date:'])
    df['Assumed GWL:'] = df['Assumed GWL:'].astype(float)
    df['Pre-Drill:'] = df['Pre-Drill:'].astype(float) 
    df['aratio'] = df['aratio'].astype(float) 
    df['CPT-ID'] = df['CPT-ID'].astype(str) 

    return None

