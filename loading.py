import glob
from time import time
import pandas as pd
import liquepy as lq
import matplotlib.pyplot as plt
from cachetools import cached, TTLCache
from filepaths import *
cache = TTLCache(maxsize = 200, ttl = 86400)
import datetime

@cached(cache)
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

    dfo = pd.DataFrame(columns = [""]*9)
    dfo.columns = headers
    for i,file in enumerate(ffps):
        name = file.split('CPT_')[-1].split('.csv')[0]
        df = pd.read_csv(file, sep = ';')
        limit = 24
        new_df = df.iloc[:limit,0:2]
        #Create a list out of the dataframe rows, and search for the corresponding values
        series = list(new_df.iloc[:,0])
    
        idcs = [i for i,x in enumerate(series) if x in headers]
        _ = ["" for i in range(len(idcs))]
        #To remake this vals thing to list? which one would be faster?
        vals = dict(zip(headers,df.iloc[idcs,1])) #Values cannot be keys since you have repeated 
                                                    #values of zeros
        cpt = lq.field.load_mpa_cpt_file(file, delimiter=";")

        #Create a list out of the dictionary values
        val_list = list(vals.values())
        val_list.extend([name,cpt])  #append cpt name and cpt object from liquepy
        #print(val_list)

        dfo.loc[i,:] = val_list #add rows iteratively from the ffps 
    
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

