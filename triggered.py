import liquepy as lq
import matplotlib.pyplot as plt
from calc import liquefaction
from read import reading
from loading import loading
import numpy as np
fp_in = "C:/Github/biotopia/input/"
fp_out = "C:/Github/biotopia/output/"



# reading.convert_folder(fp_in, fp_out, verbose=True)



dfs = loading.load_dataframe(fp_out)

cpt = dfs['Object'][0]

lf = liquefaction.run_rw1997(cpt, pga = 0.122, m_w = 0.6, gwl = 2)
#print(lf.elastic_modulus)
print(np.round(lf.i_c,2))