# This file contains the class for the summary of the CPT data

import numpy as np
import liquepy as lq
from liquefaction import run_rw1997


cpt = lq.field.load_mpa_cpt_file('CPT_H15c.csv', delimiter=';')
rw_1997 = run_rw1997(cpt, pga = 0.122, m_w = 6, gwl = 4)


ic = rw_1997.i_c
depth = rw_1997.depth

#min fos
#max fos

# for x,y in zip(rw_1997.depth, rw_1997.factor_of_safety):
#     print(x,y)

def calc_cumulative_ic(i_c):
    """
    Returns max.cumulative thickness of Ic > 2.6

    We take the ic array and find the cumulative thickness of Ic > 2.6
    We take the indeces, and find the difference between them. We then split the array if it's not 1.
    [1,1,1,2,1,1,1,5,1,1,1,7] ->
    [[1,1,1,2],[1,1,1,5],[1,1,1,7]]

    #Legacy code.
    consecutives = []
    count = 0
    for dd in range((boo.size-1)):
        if mm[dd] == 1:
            count += 1
            if dd == (boo.size-2):
                consecutives.append(count)
        else:
            consecutives.append(count)
            count = 1

    """
    mask = np.where(ic > 2.6)
    mm = np.diff(mask).flatten()
    cumuls = [x.size for x in np.split(mm, np.where(mm != 1)[0])]
    print(cumuls)
    return np.max(cumuls)

def calc_min_elev_ic(i_c):
    """
    Returns the minimum elevation of Ic > 2.6
    """
    return np.min([depth[1:][ic[1:]>2.6]])

def calc_max_elev_ic(i_c):
    """
    Returns the maximum elevation of Ic > 2.6
    """
    return np.max([depth[1:][ic[1:]>2.6]])

def calc_cumulative_fos(fos):
    """
    Returns the cumulative thickness of FOS < 1
    """
    mask = np.where(fos < 1.25)
    mm = np.diff(mask).flatten()
    cumuls = [x.size for x in np.split(mm, np.where(mm != 1)[0])]
    return np.max(cumuls)

def calc_min_fos(fos):
    """
    Returns the minimum FOS
    """
    try:
        d = np.min(depth[fos < 1.25])
    except ValueError:
        return None
    return d

def calc_max_fos(fos):
    """
    Returns the maximum FOS
    """
    try:
        d = np.max(depth[fos < 1.25])
    except ValueError:
        return None
    return d




class CPTSummary():
    def __init__(self, obj):

        self.cum_ic = calc_cumulative_ic(obj.i_c)
        self.min_elev_ic = calc_min_elev_ic(obj.i_c)
        self.max_elev_ic = calc_max_elev_ic(obj.i_c)
        self.min_fos = obj.factor_of_safety.min()
        print(self.min_fos)
        self.cum_fos = calc_cumulative_fos(obj.factor_of_safety)
        self.min_fos_elev = calc_min_fos(obj.factor_of_safety)
        self.max_fos_elev = calc_max_fos(obj.factor_of_safety)
#mindepth 2.76
#max depth 6.59

cs=CPTSummary(rw_1997)

print(cs.__dict__)


