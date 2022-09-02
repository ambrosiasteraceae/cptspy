from reading import convert_folder
from loading import load_dataframe, save_df_to_excel, convert_to_dtype
from filepaths import *
# import os
# import glob
# import liquepy as lq
# import pandas as pd

# 01.Filter Function is ready  - 99%
# 02.Loading main & header data is ready - 99%
# 03.Convert to CSV data is ready - 99%

#convert_folder(fp_in_nmdc, fp_out_nmdc, verbose = True)

#04.Load each CPT to a single data frame - 99%

df = load_dataframe(fp_out_nmdc)
#save_df_to_excel(df)
#convert_to_dtype(df)

print(df)


