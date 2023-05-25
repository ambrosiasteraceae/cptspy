# This file contains the class for the summary of the CPT data
import numpy as np


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
    mask = np.where(i_c >= 2.6)
    mm = np.diff(mask).flatten()
    cumuls = [x.size for x in np.split(mm, np.where(mm != 1)[0])]

    return np.sum(cumuls)


def calc_min_elev_ic(i_c, depth):
    """
    Returns the minimum elevation of Ic > 2.6
    """
    # a = np.min([depth[1:][i_c[1:]>2.6]])
    a = np.min([depth[i_c > 2.6]])
    return np.round(a, 2)


def calc_max_elev_ic(i_c, depth):
    """
    Returns the maximum elevation of Ic > 2.6
    """
    a = np.max([depth[i_c > 2.6]])

    return np.round(a, 2)


def calc_cumulative_fos(fos):
    """
    Returns the cumulative thickness of FOS < 1
    """
    mask = np.where(fos < 1.25)
    mm = np.diff(mask).flatten()
    cumuls = [x.size for x in np.split(mm, np.where(mm != 1)[0])]
    # return np.max(cumuls)
    return np.sum(cumuls)


def calc_min_fos(fos, depth):
    """
    Returns the minimum FOS
    """
    try:
        d = np.min(depth[fos < 1.25])
        d = np.round(d, 2)
    except ValueError:
        return None
    return d


def calc_max_fos(fos, depth):
    """
    Returns the maximum FOS
    """
    try:
        d = np.max(depth[fos < 1.25])
        d = np.round(d, 2)
    except ValueError:
        return None
    return d


class CPTSummary():
    def __init__(self, obj):
        self.max_fos_elev = calc_max_fos(obj.factor_of_safety, obj.cpt.elevation)
        self.max_ic_elev = calc_max_elev_ic(obj.i_c, obj.cpt.elevation)
        self.min_fos_elev = calc_min_fos(obj.factor_of_safety, obj.cpt.elevation)
        self.min_ic_elev = calc_min_elev_ic(obj.i_c, obj.cpt.elevation)
        self.cum_fos = calc_cumulative_fos(obj.factor_of_safety)
        self.cum_ic = calc_cumulative_ic(obj.i_c)
        min_fos = obj.factor_of_safety.min()
        self.min_fos = np.round(min_fos, 2)

    @property
    def latex_dict(self):
        # _keys = ['Max. Elevation FoS :',
        #          'Max. Elevation IC:',
        #          'Min. Elevation FoS :',
        #          'Min. Elevation IC:',
        #          'Cumulative Liq. FoS:',
        #          'Cumulative IC:',
        #          'Min. Liq. FoS:']
        # _vals = [self.max_fos_elev,
        #          self.max_ic_elev,
        #          self.min_fos_elev,
        #          self.min_ic_elev,
        #          self.cum_fos,
        #          self.cum_ic,
        #          np.round(self.min_fos, 2)]
        #        return {k: v for k, v in zip(_keys, _vals)}

        latex_table = {
            'Max. Elevation FoS :': 'max_fos_elev',
            'Max. Elevation IC:': 'max_ic_elev',
            'Min. Elevation FoS :': 'min_fos_elev',
            'Min. Elevation IC:': 'min_ic_elev',
            'Cumulative Liq. FoS:': 'cum_fos',
            'Cumulative IC:': 'cum_ic',
            'Min. Liq. FoS:': 'min_fos'}

        return {key: getattr(self, attr) for key, attr in latex_table.items()}


