import os.path

from liquefaction import run_rw1997
from load.loading import load_mpa_cpt_file, CPT
import numpy as np
import glob

folder = 'D:/04_R&D/cptspy/output/'
ffps = glob.glob(folder + '*.csv')


#
choice = np.random.choice(ffps)
#
cpt = load_mpa_cpt_file(choice)
rw = run_rw1997(cpt, pga = 0.12, m_w = 6, gwl = 0)
d = {**cpt.__dict__, **rw.__dict__}


np.savez('myarr', **d)


file =np.load('myarr.npz', allow_pickle= True)
print([key for key in file.keys()])


class CPT2(object):
    def __init__(self, depth, q_c, f_s, u_2, gwl, a_ratio=None, folder_path="<path-not-set>",
                 file_name="<name-not-set>",
                 delimiter=";", elevation=None, groundlvl = None):
        """
        A cone penetration resistance test

        Parameters
        ----------
        depth: array_like
            depths from surface, properties are forward projecting (i.e. start at 0.0 for surface)
        q_c: array_like, [kPa]
        f_s: array_like, [kPa]
        u_2: array_like, [kPa]
        gwl: float, [m]
            ground water level
        a_ratio: float,
            Area ratio
        """
        self.depth = depth
        self.q_c = q_c
        self.f_s = f_s
        self.u_2 = u_2
        self.gwl = gwl
        self.a_ratio = a_ratio
        self.folder_path = folder_path
        self.file_name = file_name
        self.delimiter = delimiter
        if groundlvl:
            self.elevation = groundlvl - depth
        else:
            self.elevation = elevation
        self._q_t = None
        self._r_f = None

    @property
    def q_t(self):
        """
        Pore pressure corrected cone tip resistance

        """
        # qt the cone tip resistance corrected for unequal end area effects, eq 2.3

        # lazy load of q_t
        if self._q_t is None:
            self._q_t = self.q_c + ((1 - self.a_ratio) * self.u_2)
        return self._q_t

    @property
    def r_f(self):
        if self._r_f is None:
            self._r_f = (self.f_s[1:] / self.q_t[1:]) * 100  # in percentages
            self._r_f = np.insert(self.r_f, 0, 0)
        return self._r_f


# depth, q_c, f_s, u_2, gwl, a_ratio=None, folder_path="<path-not-set>",
#                  file_name="<name-not-set>",
#                  delimiter=";", elevation=None, groundlvl = None
class CPT3(CPT2):
    def __init__(self, depth, q_c, f_s,  u_2, gwl,  a_ratio, folder_path, file_name, delimiter, elevation):
        super().__init__(depth, q_c, f_s,  u_2, gwl,  a_ratio, folder_path, file_name, delimiter, elevation)



class CPTloader():
    def __init__(self, file):

        temp = {}
        for key,val in file.items():
            if key in ['depth', 'q_c', 'f_s', 'u_2', 'gwl', 'a_ratio', 'folder_path', 'file_name', 'delimiter', 'elevation']:
                temp[key] = val
        if key == 'cpt':
            pass
            setattr(self,key,val)
        print(temp.keys())
        self.cpt = CPT3(**temp)

obj = CPTloader(file)
print(obj.cpt.file_name)

