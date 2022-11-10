import liquepy as lq
import matplotlib.pyplot as plt
from calc import liquefaction
from read import reading
from loading import loading
import numpy as np
from miscellaneous.plots import create_cpt_9_plot, create_cpt_before_and_after, create_plots_liq_gi_fill
from foundations.foundation import GroundImprovement



fp_in = "C:/Users/dgs/OneDrive/04_R&D/cptspy/biotopia/input/"
fp_out = "C:/Users/dgs/OneDrive/04_R&D/cptspy/biotopia/output/"


#reading.convert_folder(fp_in, fp_out, verbose=True)

dfs = loading.load_dataframe(fp_out)
# print(dfs.head(5))
create_cpt_9_plot(dfs['Object'])
# # create_cpt_before_and_after(dfs['Object'])



gi = GroundImprovement(0.8,3,11)
#
# #create_plots_liq_gi_fill(cpts,gi,fill_gamma,fill_height)
create_plots_liq_gi_fill(dfs['Object'], gi, 17,5)