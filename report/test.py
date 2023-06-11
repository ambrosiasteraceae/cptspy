import io
import glob
import matplotlib.pyplot as plt
import subprocess
import os
from pylatex import *
from pylatex.utils import NoEscape, bold
from load.loading import load_cpt_header, load_mpa_cpt_file #CREATE cpt_file module
from calc.liquefaction import run_rw1997
from calc.summary import CPTSummary
from miscellaneous.figures import *


#
def save_figure_to_memory(fig):
    # save the figure to a BytesIO object
    figfile = io.BytesIO()
    fig.savefig(figfile, format='png')
    figfile.seek(0)  # rewind to beginning of file
    return figfile  # return BytesIO object

# usage:


paths = ['C:/Users/dragos/Documents/GitHub/cptspy/output/CPT_L21d.csv']

pga = 0.122
m_w = 6
GWL = 0.6
gwl = 0.6
scf = 1.30
my_list = []
for path in paths:
    cpt = load_mpa_cpt_file(path, scf=scf)
    gwl = cpt.elevation[0] - GWL
    my_list.append((path, gwl, cpt.elevation[0]))
    rw_1997 = run_rw1997(cpt, pga=pga, m_w=m_w, gwl=gwl)
    cpth = load_cpt_header(path)
    cpts = CPTSummary(rw_1997)

fig, sps = plt.subplots(nrows=1, ncols=3, figsize=(16, 10))
create_fos_and_index_plot(sps, rw_1997)
figfile = save_figure_to_memory(fig)




