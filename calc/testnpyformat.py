from liquefaction import run_rw1997
from loading.loading import load_mpa_cpt_file
import numpy as np
import glob
# folder = 'D:/04_R&D/cptspy/output/'
# ffps = glob.glob(folder + '*.csv')


#
# choice = np.random.choice(ffps)
#
# cpt = load_mpa_cpt_file(choice)
# #
# rw = run_rw1997(cpt, pga = 0.12, m_w = 6, gwl = 0)


# np.savez('myarr', **rw.__dict__)


file = np.load('myarr.npz', allow_pickle= True)


# for k,v in file.items():
#     print(k,v)

# print([key for key in file.keys()])
# print(file['cpt'], type(file['cpt']))


class Reader():
    def __init__(self, npzfile):
        for key,val in npzfile.items():
            setattr(self, key, val)

obj=Reader(file)

print(obj.depth, obj.factor_of_safety)