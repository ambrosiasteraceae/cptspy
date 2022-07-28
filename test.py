from reading import convert_folder
from filepaths import *
import os
import glob
import liquepy as lq

#Filter Function is ready  - 100%
#Loading main & header data is ready - 100%
# convert_folder(fp_in_nmdc, fp_out_nmdc, verbose = True)

#Loading multiple data frames



cpt = lq.field.load_cpt_from_file(ffps[index], delimiter=";")

