import numpy as np
import liquepy as lq
from fig import timed


def calc_qt(qc, ar, u2):
    """

    :param qc: kPa, cone tip resistance
    :param ar: -, area ratio
    :param u2: kPa, water pressure beneath cone tip
    :return:
    """
    # qt the cone tip resistance corrected for unequal end area effects, eq 2.3
    return qc + ((1 - ar) * u2)


def calc_sigma_v(depths, gammas, gamma_predrill=17.0):
    """
    Calculates the vertical stress

    Note: properties are forward projecting
    """
    predrill_depth = depths[0]
    depth_incs = depths[1:] - depths[:-1]
    depth_incs = np.insert(depth_incs, 0, depth_incs[0])
    sigma_v_incs = depth_incs * gammas
    sigma_v = np.cumsum(sigma_v_incs) + predrill_depth * gamma_predrill
    return sigma_v


def calc_pore_pressure(depth, gwl, unit_water_wt):
    pore_pressure = np.where(depth > gwl, (depth - gwl) * unit_water_wt, 0.0)
    return pore_pressure


def calc_sigma_veff(sigma_v, pore_pressure):
    sigma_veff = abs(sigma_v - pore_pressure)
    return sigma_veff


def calc_rd(depth):
    """
    Returns rd from CPT
    For the moment only works for a CPT depth < 23meters
    """
    rd = np.where(depth < 9.15, 1.0 - 0.00765 * depth, 1.174 - 0.0267 * depth)
    return rd


def calc_unit_dry_weight(fs, q_t, p_a, unit_water_wt):
    """
    Estimate the unit weight of the soil.

    Ref: https://www.cpt-robertson.com/PublicationsPDF/Unit%20Weight%20Rob%20%26%20Cabal%20CPT10.pdf

    Parameters
    ----------
    fs: array_like
        CPT skin friction (kPa)
    q_t: array_like
        CPT cone tip resistance (kPa)
    p_a: float
        Atmospheric pressure (kPa)
    unit_water_wt: float
        Unit weght of water

    Returns
    -------

    """
    # eq Robertson pag 37- CPT guide
    # unit_water_wt = 9.81
    np.clip(q_t, 1e-10, None, out=q_t)
    r_f = np.clip((fs / q_t) * 100, 0.1, None)
    min_unit_weight = 1.5 * unit_water_wt  # minimum value obtained in presented results
    max_unit_weight = 4.0 * unit_water_wt  # maximum value obtained in presented results
    soil_unit_wt = np.clip((0.27 * np.log10(r_f) + 0.36 * np.log10(q_t / p_a) + 1.236) * unit_water_wt, min_unit_weight,
                           max_unit_weight)
    return soil_unit_wt


def calc_big_f_values(fs, qt, sigma_v):
    # qt is in kPa, so it's not necessary measure unit transformation
    return (fs / (qt - sigma_v)) * 100


def calc_big_q_values(qt, sigma_v, sigma_veff, p_a, n_val=0.5):
    """
    Eq. 2.26
    :param c_n: CN
    :param qt:
    :param sigmav:
    :return:
    """
    # return (qt - sigmav) / 100 * c_n   # this is different to eq 2.26
    return (qt - sigma_v) / p_a * (p_a / sigma_veff) ** n_val


def calc_i_c(big_q, big_f):
    """
    Calculates the index parameter of the soil

    Eq. 2.26

    :param big_q: float or array,
    :param big_f: float or array,
    :return:
    """

    if big_f <= 0.1:
        big_f = 0.1
    if big_q <= 1:
        big_q = 1
    return ((3.47 - np.log10(big_q)) ** 2 + (1.22 + np.log10(big_f)) ** 2) ** 0.5


def calc_csr(sigma_veff, sigma_v, pga, rd):
    """
    Cyclic stress ratio from CPT
    """
    return 0.65 * (sigma_v / sigma_veff) * rd * pga


@timed.timed
def calc_dependent_variables(sigma_v, sigma_veff, f_s, p_a, q_t):
    """
    Iteratively calculate_volumetric strain parametrs as they are interedependet
    """

    num_depth = len(sigma_v)
    m_values = np.ones(num_depth)  # create an array of ones
    cn_values = np.zeros(num_depth)

    big_q = np.ones(num_depth)
    big_f = np.ones(num_depth)
    i_c = np.ones(num_depth)

    for dd in range(0, num_depth):
        n_val = 1.00
        while True:
            big_q[dd] = calc_big_q_values(q_t[dd], sigma_v[dd], sigma_veff[dd], p_a, n_val=n_val)
            big_f[dd] = calc_big_f_values(f_s[dd], q_t[dd], sigma_v[dd])
            i_c[dd] = calc_i_c(big_q[dd], big_f[dd])
            n_val_current = max(0.5, 0.381 * i_c[dd] + 0.05 * (sigma_veff[dd] / p_a) - 0.15)
            # print(n_val, 0.381 * i_c[dd] + 0.05 * (sigma_veff[dd] / p_a) - 0.15)
            if n_val - n_val_current < 0.01:
                break
            else:
                n_val = n_val_current
        # print("exit 2nd loop,",n_val, f'{n_val_current:.2f}', n_val - n_val_current)
    return big_q, big_f, i_c


def calc_k_sigma(i_c, big_f):
    """
    Returns k_sigma
    i_c values higher than 2.6 and lower than 1.64 have 1
    """
    cond_1 = (i_c <= 1.64) | (i_c > 2.6)
    cond_2 = ((i_c > 1.64) & (i_c <= 2.36)) & (big_f < 0.5)
    k_sigma_cond_2 = np.where(cond_2, 1,
                       5.581 * i_c ** 3 - 0.403 * i_c ** 4 - 21.63 * i_c ** 2 + 33.75 * i_c - 17.88)

    k_sigma = np.where(cond_1, 1, k_sigma_cond_2)

    return k_sigma


    
def calc_crr_m7p5(big_q_cs):
    
    crr = np.where(big_q_cs < 50,
                   0.833 * big_q_cs / 1000 + 0.05,
                   93 * big_q_cs ** 3 / 1000 + 0.08)
    return crr
def calc_msf(m_w):
    """
    Returns magnitude scaling factor
    """
    return 174 / (m_w ** 2.56)

class RobertsonWride1997CPT(object):

    def __init__(self, cpt, gwl=None, pga=0.25, m_w=None, **kwargs):
        """
        Performs the Boulanger and Idriss triggering procedure for a CPT profile

        ref: Boulanger:2014id

        Parameters
        ----------

        gwl: float, m,
            ground water level below the surface
        pga: float, g,
            peak ground acceleration
        m_w: float, -,
            Earthquake magnitude
        a_ratio: float, -, default=0.8
            Area ratio
        magnitude: float, -,
            Earthquake magnitude (deprecated)
        i_c_limit: float, -, default=2.6
            Limit of liquefiable material
        s_g: float or array_like, -, default=2.65
            Specific gravity
        s_g_water: float, -, default=1.0
            Specific gravity of water
        p_a: float, -, kPa, default=101
            Atmospheric pressure
        """

        magnitude = kwargs.get("magnitude", None)
        i_c_limit = kwargs.get("i_c_limit", 2.6)
        self.s_g = kwargs.get("s_g", 2.65)
        self.s_g_water = kwargs.get("s_g_water", 1.0)
        self.p_a = kwargs.get("p_a", 101.)  # kPa
        self.c_0 = kwargs.get("c_0", 2.8)
        saturation = kwargs.get("saturation", None)
        unit_wt_method = kwargs.get("unit_wt_method", "robertson2009")
        gamma_predrill = kwargs.get("gamma_predrill", 17.0)
        if gwl is None and cpt.gwl is not None:
            gwl = cpt.gwl

        if m_w is None:
            if magnitude is None:
                self.m_w = 7.5
        else:
            self.m_w = m_w

        unit_water_wt = self.s_g_water * 10
        self.npts = len(cpt.depth)
        self.depth = cpt.depth
        self.cpt = cpt
        # self.q_c = cpt.q_c
        # self.f_s = cpt.f_s
        # self.u_2 = cpt.u_2
        self.gwl = gwl
        self.pga = pga
        self.a_ratio = cpt.a_ratio
        if cpt.a_ratio is None:
            self.a_ratio = 0.8
        self.i_c_limit = i_c_limit

        self.q_t = calc_qt(self.cpt.q_c, self.a_ratio, self.cpt.u_2)  # kPa

        if saturation is None:
            self.saturation = np.where(self.depth < self.gwl, 0, 1)
        else:
            self.saturation = saturation
        if unit_wt_method == "robertson2009":
            self.unit_wt = calc_unit_dry_weight(self.cpt.f_s, self.q_t, self.p_a, unit_water_wt)
        else:
            raise ValueError(
                "unit_wt_method should be: 'robertson2009'  %s" % unit_wt_method)

        self.sigma_v = calc_sigma_v(self.depth, self.unit_wt, gamma_predrill)
        self.pore_pressure = calc_pore_pressure(self.depth, self.gwl, unit_water_wt)
        self.sigma_veff = calc_sigma_veff(self.sigma_v, self.pore_pressure)
        if self.sigma_veff[0] == 0.0:
            self.sigma_veff[0] = 1.0e-10


        self.big_q, self.big_f, self.i_c = calc_dependent_variables(self.sigma_v, self.sigma_veff, self.cpt.f_s,
                                                                    self.p_a, self.q_t)

        self.k_sigma = calc_k_sigma(self.i_c, self.big_f)
        self.big_q_cs = self.big_q * self.k_sigma
        self.crr_m7p5 = calc_crr_m7p5(self.big_q_cs)
        self.rd = calc_rd(self.depth)
        self.csr = calc_csr(self.sigma_veff, self.sigma_v, pga, self.rd)
        self.msf = calc_msf(self.m_w)


        fs_unlimited = self.csr / self.crr_m7p5
        print(fs_unlimited)
        fos = np.where(fs_unlimited > 2, 2, fs_unlimited)
        self.factor_of_safety = np.where(self.i_c <= self.i_c_limit, fos, 2.25)
        # print(self.big_f[0])
        # self.k_sigma = calc_k_sigma()
        # self.big_q_cs = calc_big_q_cs()


cpt = lq.field.load_mpa_cpt_file("CPT_H15c.csv", delimiter=";")
#bi2014 = lq.trigger.run_bi2014(cpt, pga=0.33, m_w=6)
lf = RobertsonWride1997CPT(cpt)
print(lf.big_q_cs)
print(lf.factor_of_safety)

