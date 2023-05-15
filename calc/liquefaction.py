import numpy as np
import liquepy as lq
from miscellaneous import timed
import matplotlib.pyplot as plt
from loading import loading


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


# @timed.timed
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


def calc_phi(i_c, big_q):
    """
    Returns friction angle array based on Jefferies and Been (2006)
    """
    k_c = np.where(i_c <= 1.64, 1,
                   5.581 * i_c ** 3 - 0.403 * i_c ** 4 - 21.63 * i_c ** 2 + 33.75 * i_c - 17.88)
    q_tn_cs = np.abs(big_q * k_c)
    # _phi = 33 + 15.84 * np.log10(q_tn_cs) - 26.88
    _phi = np.nan_to_num(33 + 15.84 * np.log10(q_tn_cs) - 26.88, nan=33)

    return np.where(_phi > 45, 45, _phi)


def calc_young_modulus_factor(i_c, big_q):
    """
   Returns alfa_e for young modulus coefficient.
   This is for I_c > 2.6 (fine soils)
   See eq. ->                for reference
    """
    _alfa_e = 0.015 * np.power(10, (0.55 * i_c + 1.68))
    alfa_ee = np.where(_alfa_e > 7, 7, _alfa_e)
    alfa_bb = np.where((big_q < 7) & (big_q > 0), big_q, 7)
    alfa_e = np.where(i_c < 2.6, alfa_ee, alfa_bb)
    return alfa_e


def calc_young_modulus(alfa_e, q_t, sigma_v):
    return alfa_e * (np.where(q_t <= 0.1, np.nan, q_t) - sigma_v)


def calc_crr_m7p5(big_q_cs):
    crr = np.where(big_q_cs < 50,
                   0.833 * big_q_cs / 1000 + 0.05,
                   93 * (big_q_cs / 1000) ** 3 + 0.08)
    return crr


def calc_msf(m_w):
    """
    Returns magnitude scaling factor
    """
    return 174 / (m_w ** 2.56)


def rolling_mean(q_c, pts=41):
    return np.convolve(q_c, np.ones(pts), 'same') / pts


def calc_s_u(q_t, sigma_v, nkt=18):
    return (q_t - sigma_v) / nkt


def calc_permeability(i_c):
    """
    Returns permeability
    """

    k_perm = np.ones(len(i_c))

    cond_1 = np.where((1 < i_c) & (i_c <= 3.27))
    cond_2 = np.where((3.27 < i_c) & (i_c < 4))
    cond_3 = np.where((i_c < 1) & (i_c > 4))

    k_perm[cond_1] = np.power(10, 0.952 - 3.04 * i_c[cond_1])
    k_perm[cond_2] = np.power(10, -4.52 - 1.37 * i_c[cond_2])
    k_perm[cond_3] = np.nan

    return k_perm


class RobertsonWride1997CPT(object):

    def __init__(self, cpt, gwl=None, pga=0.25, m_w=None, **kwargs):
        """
        Performs the Roberston and Wride triggering procedure for a CPT profile

        ref: R&W:1997id

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
        self.phi = calc_phi(self.i_c, self.big_q)

        self.alfa_e = calc_young_modulus_factor(self.i_c, self.big_q)
        self.elastic_modulus = calc_young_modulus(self.alfa_e, self.q_t, self.sigma_v)
        self.permeability = calc_permeability(self.i_c)
        self.s_u = calc_s_u(self.q_t, self.sigma_v)
        self.k_sigma = calc_k_sigma(self.i_c, self.big_f)
        self.big_q_cs = self.big_q * self.k_sigma
        self.crr_m7p5 = calc_crr_m7p5(self.big_q_cs)
        self.rd = calc_rd(self.depth)
        self.csr = calc_csr(self.sigma_veff, self.sigma_v, pga, self.rd)
        self.msf = calc_msf(self.m_w)

        fs_unlimited = self.crr_m7p5 / self.csr * self.msf

        fos = np.where(fs_unlimited > 2, 2, fs_unlimited)
        self.factor_of_safety = np.where(self.i_c <= self.i_c_limit, fos, 2.25)


def run_rw1997(cpt, pga, m_w, gwl=None, p_a=101., cfc=0.0, i_c_limit=2.6, gamma_predrill=17.0, c_0=2.8,
               unit_wt_method='robertson2009', s_g=2.65, s_g_water=1.0, saturation=None):
    """
    Runs the Boulanger and Idriss (2014) triggering method.

    Parameters
    ----------
    cpt: liquepy.field.CPT,
        ground water level below the surface
    pga: float, g,
        peak ground acceleration
    m_w: float, -,
        Earthquake magnitude
    gwl: float, m,
        depth to ground water from surface at time of earthquake
    p_a: float, kPa, default=101
        Atmospheric pressure
    cfc: float, -, default=0.0
        Fines content correction factor for Eq 2.29
    i_c_limit: float, -, default=2.6
        Limit of liquefiable material
    gamma_predrill: float, kN/m3, default=17.0
        Unit weight of soil above pre-drill depth
    c_0: float, -, default=2.8
        Factor that adjusts the CRR-vs-qc1ncs relationship
    unit_wt_method: str, -, default='robertson2009'
        Method used to determine unit weight
    s_g: float or array_like, -, default=2.65
        Specific gravity
    s_g_water: float, -, default=1.0
        Specific gravity of water
    saturation: array_like or None
        Saturation ratio for each depth increment

    Returns
    -------
    BoulangerIdriss2014CPT()
    """

    return RobertsonWride1997CPT(cpt, gwl=gwl, pga=pga, m_w=m_w, cfc=cfc, i_c_limit=i_c_limit, s_g=s_g,
                                 s_g_water=s_g_water, p_a=p_a,
                                 saturation=saturation, unit_wt_method=unit_wt_method, gamma_predrill=gamma_predrill,
                                 c_0=c_0)


class RobertsonWride1997GI(object):
    """
    Performs the post improvement liquefaction triggering analysis considering thed presence
    of inclusions (CMC & Stone Columns). It uses the appraoch of Baez & Martinez.


    Parameters
    ----------
        rw1997: RobertsonWride1997CPT object,

        gi: ground improvement object,

    Returns
    -----------
        rw1997_gi object

    """

    def __init__(self, rw1997, gi):
        self.depth = rw1997.depth
        self.gi = gi
        self.csr = np.where(self.depth <= gi.depth,
                            rw1997.csr * self.gi.ssr_factor,
                            rw1997.csr)  # Taking into account depth of ground improvement
        fs_unlimited = rw1997.crr_m7p5 / self.csr * rw1997.msf
        fos = np.where(fs_unlimited > 2, 2, fs_unlimited)
        self.factor_of_safety = np.where(rw1997.i_c <= rw1997.i_c_limit, fos, 2.25)


def run_rw1997_gi(rw1997, gi):
    """
    Returns RW1997GroundImprovement
    """
    return RobertsonWride1997GI(rw1997=rw1997, gi=gi)


class RobertsonWride1997CPTFILL(RobertsonWride1997CPT):
    def __init__(self, cpt, gwl=None, pga=0.25, m_w=None, fill_height=None,
                 fill_gamma=None, k_factor=0.25, **kwargs, ):
        super().__init__(cpt, gwl=gwl, pga=pga, m_w=m_w, **kwargs)

        self.fill_height = fill_height
        self.fill_gamma = fill_gamma
        self.k_factor = k_factor

        self.sigma_fill = fill_height * fill_gamma  # 1
        self.sigma_veff_new = self.sigma_veff + self.sigma_fill  # 2
        self.sigma_v_new = self.sigma_v + self.sigma_fill  # 3

        self.factor = k_factor * (self.sigma_veff_new - self.sigma_veff) / self.sigma_veff  # 4
        self.cpt.q_c = self.factor * self.cpt.q_c + self.cpt.q_c  # 5
        self.cpt.f_s = self.factor * self.cpt.f_s + self.cpt.f_s  # 6
        self.q_t = calc_qt(self.cpt.q_c, self.a_ratio, self.cpt.u_2)  # 7

        self.big_q, self.big_f, self.i_c = calc_dependent_variables(self.sigma_v_new, self.sigma_veff_new, self.cpt.f_s,
                                                                    self.p_a, self.q_t)  # 8
        self.k_sigma = calc_k_sigma(self.i_c, self.big_f)  # 9
        self.big_q_cs = self.big_q * self.k_sigma  # 10
        self.crr_m7p5 = calc_crr_m7p5(self.big_q_cs)  # 11
        self.rd = self.calc_rd(self.depth, self.fill_height)  # 12
        self.csr = calc_csr(self.sigma_veff_new, self.sigma_v_new, pga, self.rd)  # 13
        self.msf = calc_msf(self.m_w)  # 14

        fs_unlimited = self.crr_m7p5 / self.csr * self.msf  # 15

        fos = np.where(fs_unlimited > 2, 2, fs_unlimited)  # 16
        self.factor_of_safety = np.where(self.i_c <= self.i_c_limit, fos, 2.25)  # 17

    def calc_rd(self, depth, fill_height):
        """
        Returns rd from CPT
        For the moment only works for a CPT depth < 23meters
        """
        # depth += fill_height
        rd_depth = depth + fill_height
        rd = np.where(rd_depth < 9.15, 1.0 - 0.00765 * rd_depth, 1.174 - 0.0267 * rd_depth)
        return rd


def run_rw1997_fill(cpt, gwl=None, pga=0.25, m_w=None, fill_height=None,
                 fill_gamma=None, k_factor=0.25, **kwargs):
    return RobertsonWride1997CPTFILL(cpt, gwl=gwl, pga=pga, m_w=m_w, fill_height=fill_height,
                 fill_gamma=fill_gamma, k_factor=k_factor, **kwargs)



# from foundations.foundation import GroundImprovement
#
# gi = GroundImprovement(0.6,3,5)
cpt = lq.field.load_mpa_cpt_file('CPT_H15c.csv', delimiter=';')
# #RobertsonWride1997CPTFILL(cpt, pga=0.122, m_w=6, gwl=2, fill_height=5, fill_gamma=17)
rw_1997 = run_rw1997(cpt, pga = 0.122, m_w = 6, gwl = 4)
# rw_fill = run_rw1997_fill(cpt, pga = 0.122, m_w = 6, gwl = 2, fill_gamma= 17, fill_height= 8)
# rw_gi = run_rw1997_gi(rw_1997,gi)
#
# plt.plot(rw_1997.factor_of_safety, -cpt.depth, label = 'R&W')
# plt.plot(rw_fill.factor_of_safety, -cpt.depth, label = 'R&W Fill')
# plt.plot(rw_gi.factor_of_safety, -cpt.depth, label ='R&W GI')
#
# plt.legend()
# plt.show()
print([(x,y) for x,y in zip (rw_1997.cpt.q_c/10**3, rw_1997.cpt.f_s/rw_1997.q_t * 100)])

from miscellaneous import figures


figures.create_soil_index_plot(rw_1997)
plt.show()



