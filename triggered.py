import liquepy as lq
import matplotlib.pyplot as plt
from calc import liquefaction
from read import reading
from loading import loading
import numpy as np
from miscellaneous.plots import create_cpt_9_plot
fp_in = "C:/Users/dgs/OneDrive/04_R&D/cptspy/biotopia/input/"
#fp_out = "C:/Github/biotopia/output/"
fp_out = "C:/Users/dgs/OneDrive/04_R&D/cptspy/biotopia/output/"


#reading.convert_folder(fp_in, fp_out, verbose=True)



dfs = loading.load_dataframe(fp_out)
#print(dfs)

create_cpt_9_plot(dfs['Object'])

#cpt = dfs['Object'][0]

#f = liquefaction.run_rw1997(cpt, pga = 0.122, m_w = 0.6, gwl = 2)
#print(lf.elastic_modulus)
#print(np.round(lf.i_c,2))