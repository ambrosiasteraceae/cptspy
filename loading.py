import glob
import pandas as pd
import matplotlib.pyplot as plt

import liquepy as lq
from filepaths import *
from time import time


def load_dataframe(out_fp):
    """"

    Iterates through the output folder, looking for all csv files
    It reads file by file, looking through the contents of header
    data.

    Example:
     "Easting" : "2600985"
     "Assumed GWL" : 0.00
    
    A header list is created and it searches for the values that 
    reference the headers. It also loads the CPT data as a CPT object 
    for further processing. Every file is appended in the DataFrame
    row by row.

   
    
    Parameters
    ------------
    out_fp : str
        Folder path of existing  CPT files in CSV format
    save_fp : str 
        Folder path where dataframe files should be saved
    
    Returns 
    ------------
    DataFrame
        Data frame contains
    
    See Also
    ------------
    load_mpa_cpt_file()

    """

    ffps = glob.glob(out_fp + "*.csv") #

    headers = ['Date:', 'Assumed GWL:', 'groundlvl','Pre-Drill:', 'Easting', 'Northing',
                'aratio','CPT-ID','Object']
    limit = 24
    hh = headers[0:-2] #Up to but not including the 'CPT-ID' & 'Object'. T
    dfo = pd.DataFrame(columns = [""]*9)
    dfo.columns = headers
    for i,file in enumerate(ffps):
        #print(file)
        name = file.split('CPT_')[-1].split('.csv')[0]
        df = pd.read_csv(file, sep = ';')
        
        new_df = df.iloc[:limit,0:2]

        
        series1=list(new_df.iloc[:,0]) #Store  all 1st row variables  from DataFrame
        series2=list(new_df.iloc[:,1]) #Store all 2nd row values from DataFrame
        dicty = dict(zip(series1,series2))

        l=[]        #Store the dict values based on the order of appeareance 
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

    Save a DataFrame to excel.
    
    
    Parameters
    ------------
    df : DataFrame
    name : str
        Name of file, defaults to "00_Header&Data.xlsx"

    Returns 
    ------------
    None    

    #TODO: Add output file location
    """

    

    excel_file = pd.ExcelWriter(name)
    df.to_excel(excel_file, sheet_name = 'df')
    excel_file.save()

    return None

def convert_to_dtype(df):

    """

    Convert different column types to their respective types,
    especially time to datetime type for future manipulation.

    Parameters
    -------------
    df : DataFrame
        
    Returns
    -------------
    None


    #TODO: Check to see if .astype(float) & .astype(str) is redundant

    """
    df['groundlvl'] = df['groundlvl'].astype(float)
    df['Date:'] = pd.to_datetime(df['Date:'])
    df['Assumed GWL:'] = df['Assumed GWL:'].astype(float)
    df['Pre-Drill:'] = df['Pre-Drill:'].astype(float) 
    df['aratio'] = df['aratio'].astype(float) 
    df['CPT-ID'] = df['CPT-ID'].astype(str) 

    return None

