import numpy as np
import liquepy as lq
from foundations.foundation import FoundationObject


def raft_vertical_stress(lf, fd, delta_p, incs):
    """"
    Returns raft vertical stress as per the bousinesq theory.
    However, note that it returns for
    """
    # Following equation
    a = fd.short
    b = fd.long
    z = np.arange(lf.depth[0] + fd.depth, lf.depth[-1] + incs,
                  incs)  # In case we have found. depth, new depth will start below footing

    r_1 = np.sqrt(a ** 2 + z ** 2)
    r_2 = np.sqrt(b ** 2 + z ** 2)
    r_3 = np.sqrt(a ** 2 + b ** 2 + z ** 2)

    vertical_stress = delta_p / (2 * np.pi) * (
            np.arctan(a * b / (z * r_3)) + (a * b * z / r_3) * (1 / r_1 ** 2 + 1 / r_2 ** 2))

    return vertical_stress


def raft_settlement(vertical_stress, young_modulus, incs):
    return vertical_stress / young_modulus * incs


fd = FoundationObject(2, 2, 0, 0)
cpt = lq.field.load_mpa_cpt_file("C:/Users/dgs/OneDrive/04_R&D/cptspy/output/CPT_H16d.csv", delimiter=";")
lf = lq.trigger.run_bi2014(cpt, pga=0.25, m_w=7.5, gwl=2.5)

print(raft_vertical_stress(lf, fd, 150, 0.01))


#Write function to refer to different settlement func:

def calc_raft_settlement():
    pass

def calc_footing_settlement():
    pass


def calc_settlement(lf,fd,load,years):
    if fd.shape == 'raft':
        return calc_raft_settlement
    else:
        return calc_footing_settlement