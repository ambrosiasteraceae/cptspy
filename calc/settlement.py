import numpy as np
from fig.log import log
from fig.timed import timed


def calculate_peak_settlement_indexes(fd):
    """
    Calculate the limit variables of the influence factor variables.
    They start from ground level e.g. taking fd.depth into account.


    Refer to strain influence graph for more info.

    Parameters
    ---------
    fd : Foundation_Object
        fd.short is for width

    Returns
    ----------
    z_top: int
        Abcissa element of the strain influence graph ranges between [0.1:I_zp]
    z_bottom: int
        End of settlement influence
    zp: int
        Peak level @ which i_z factor is maximum
    """
    if fd.radius:
        z_top = 0.1
        zp = 0.5 * fd.radius + fd.depth
        z_bottom = 2 * fd.radius + fd.depth

    else:
        ratio = fd.long / fd.short
        if ratio > 10:
            zp = fd.short + fd.depth  # Absolute Peak elevation of strain influence
            z_top = 0.2
            z_bottom = 4 * fd.short + fd.depth

        elif ratio <= 1:
            z_top = 0.1
            zp = 0.5 * fd.short + fd.depth
            z_bottom = 2 * fd.short + fd.depth

        else:  # if ratio is between 1 & 10
            z_top = np.interp(ratio, [1, 10], [0.1, 0.2])
            zp = np.interp(ratio, [1, 10], [0.5, 1]) * fd.short + fd.depth
            z_bottom = np.interp(ratio, [1, 10], [2, 4]) * fd.short + fd.depth

    return z_top, z_bottom, zp


def calculate_correction_factors(fd, overburden, delta, years):
    """
    Calculate the correction factors

    Parameters
    ------------

    fd: Foundation_object
    overburden: ndarray or int
    delta: ndarray or int
    years : int

    Returns:
    -----------

    c1,c2,c3 : int
        Correction factors
    """
    # EMBEDMENT FACTOR
    c_1 = max(1 - 0.5 * (overburden / delta), 0.5)
    # CREEP FACTOR
    if years == 0:
        c_2 = 1.0
    else:
        c_2 = 1.0 + 0.2 * np.log10(years / 0.1)
    # SHAPE OF FOOTING CORRECTION
    c_3_dict = {"circular": 1,
                "square": 1.2,
                "raft": 1.2,  # To be confirmed
                "strip": 1.75}
    c_3 = c_3_dict[fd.shape]
    return c_1, c_2, c_3


def calculate_net_pressure(lf, fd, load, gamma=0):
    """
    Returns the net footing pressure (load - overburden) and overburden (sigma_1) pressure

    Futures:
    #TODO: Implement method for prefillingn in case of fd.depth>2.
    """

    if gamma:
        return NotImplemented('Future build will implement gamma. Requires calls to sigma_veff')

    if fd.depth > 0:
        overburden = lf.sigma_veff[np.where(lf.depth == fd.depth)]
    else:
        overburden = 0
    delta_p = load - overburden
    return delta_p, overburden


def calculate_strain_influence_peak(lf, zp, delta_p):
    """
    Returns strain_influence_peak

   """
    mask = np.where(lf.depth == zp)
    sigma_v2 = lf.sigma_veff[mask]  # Effective stress pressure at peak index
    i_zp = 0.5 + 0.1 * (delta_p / sigma_v2) ** 0.5
    return i_zp


def calculate_iz(lf, fd, z_top, zp, z_bottom, i_zp):
    """
    Returns the strain influence factor.

    iz AB & iz BC taken from (y-ya) / (yb-ya) = (x-xa) / (xb - xa)
    Note that It starts from the depth of CPT and not  depth of footing.

    Future
    -------
    #Test this properly. How? /:(
    #EDIT. I think it works for all cases now!

    Parameters
    ----------
    lf: LiquefyObject
    fd: Foundation_Object
    z_top, zp, z_bottom: int
    i_zp: int
        Strain influence peak

    Returns
    ---------
    iz: ndarray or int
    """
    iz = np.zeros(lf.depth.size)
    incs = lf.depth[1] - lf.depth[0]
    limit = lf.depth[-1]

    if z_bottom < limit:
        limit = z_bottom  # We limit our CPT

    elevs = np.arange(lf.depth[0] + fd.depth, limit + incs, incs)  # We start a new array counting from  fd.de
    log(z_bottom, zp, z_top)

    iz_ab = ((i_zp - 0.1) * (elevs[elevs <= zp] - fd.depth)) / (zp - fd.depth) + 0.1
    iz_bc = i_zp + (-i_zp * (elevs[np.where(elevs > zp)] - zp)) / (z_bottom - zp)
    abbc = np.hstack((iz_ab, iz_bc))
    indexes = np.where((lf.depth >= fd.depth + lf.depth[0]) & (lf.depth <= limit))
    #     if verbose:
    #         log("lf.depth:",lf.depth.size)
    #         log("Elevs:",elevs.size)
    #         log("<=zp",elevs[elevs<=zp].size)
    #         log("zp>",elevs[np.where(elevs > zp)].size)
    #         log("Indexes:",len(indexes[0]))
    #         log("abbc:",abbc.size)
    #         log("iz",iz)
    iz[indexes] = abbc

    return iz


def calculate_young_modulus(lf):
    """
   Returns alfa_e for young modulus coefficient.
   This is for I_c > 2.6 (fine soils)
   See eq. ->                for reference
    """
    _alfa_e = 0.015 * np.power(10, (0.55 * lf.i_c + 1.68))
    alfa_ee = np.where(_alfa_e > 7, 7, _alfa_e)
    alfa_bb = np.where((lf.big_q < 7) & (lf.big_q > 0), lf.big_q, 7)
    alfa_e = np.where(lf.i_c < 2.6, alfa_ee, alfa_bb)
    return alfa_e


def calculate_consolidation(lf, alfa_e, incs, i_z, overburden, delta_p):
    """
    Returns consolidation settlement on layers that are with fine soils
    I_c > 2.6.

    Parameters:
    -----------
    alfa_e:
    lf:
    ins:
    i_z:
    overburden:
    delta_p:

    Returns:
    ----------
    consolidation_settlement : ndarray

    """
    alfa_m = 1.35 * alfa_e  # Can this be over 7?
    alfa_m = np.where(alfa_m > 7, 7, alfa_m)
    constrained_modulus = alfa_m * (lf.q_t - overburden)
    e_0 = 0.9  # I've seen e_0 of 0.65
    c_c = 2.3 * (1 + e_0) * lf.sigma_veff / constrained_modulus
    consolidation = (c_c * incs / (1 - e_0)) * np.log10((lf.sigma_veff + i_z * delta_p) / lf.sigma_veff)
    return np.where(lf.i_c > 2.6, consolidation, 0)


@timed
def settlement(lf, fd, load, years, verbose=True, val_limit=0.025):
    """
    Calculate settlement based on Schmertmann method.
    Calculate elastic, creep settlement and consolidation
    only for layers that have an I_c value > 2.6.

    Please see Schmertmann -> CPT 2014 Guide

    Future:
    ---------
    Should load a soil profile with rock layers
    Other times should simply return settlement for
    soil profile only!

    It calculates the Iz influence factor of an isolated
    footing. Interpolates for l/b in 1...10 range.

    Parameters
    -----------

    fd :  Foundation_Object
    lf : Liquepy_Object
    load : int / float
        Load acting on top of foundation. Units in kPa
    years : int
        Numbers of years
    verbose : bool
        Prints log to console if true

    Returns
    -----------
    dict(settlement, elastic, creep, consolidation, iz, overburden,
            delta_p, i_zp, zp, z_top, z_bottom, c_1, c_2, c_3, alfa_e)
    """

    # TODO: Implement GammaFill in case of required future fill
    # TODO: Implement return error for not calculated?

    if fd.depth > lf.depth[-1]:
        raise ValueError("Foundation depth is higher than CPT depth!")
    if fd.short > lf.depth[-1]:
        raise ValueError("Foundation width is higher than CPT depth!")
    incs = lf.depth[1] - lf.depth[0]
    delta_z = np.ones(lf.depth.size) * incs
    lf.depth = np.round(lf.depth, 2)  # You can test this. Or you can apply this when loading from CPT's

    # Elastic + Creep
    z_top, z_bottom, zp = calculate_peak_settlement_indexes(fd)
    delta_p, overburden = calculate_net_pressure(lf, fd, load)
    c_1, c_2, c_3 = calculate_correction_factors(fd, overburden, delta_p, years)
    i_zp = calculate_strain_influence_peak(lf, zp, delta_p)
    iz = calculate_iz(lf, fd, z_top, zp, z_bottom, i_zp)
    alfa_e = calculate_young_modulus(lf)
    young_modulus = alfa_e * (np.where(lf.q_t <= 0.1, np.nan, lf.q_t) - overburden)  # q_c is 0 at start,

    elastic = (c_1 * delta_p * iz / (c_3 * young_modulus) * delta_z)
    creep = elastic * (c_2 - 1)
    consolidation = calculate_consolidation(lf, alfa_e, incs, iz, overburden, delta_p)

    settlement = elastic + creep + consolidation
    settlement = np.cumsum(settlement[::-1])

    if max(settlement[::-1]) > val_limit:

        result = "Value exceeded"
    else:
        result = "Ok"

    args = [settlement, elastic, creep, consolidation, iz, overburden, delta_p, i_zp, zp, z_top, z_bottom, c_1, c_2,
            c_3,
            alfa_e]
    cols = ['settlement', 'elastic', 'creep', 'consolidation', 'iz', 'overburden',
            'delta_p', 'i_zp', 'zp', 'z_top', 'z_bottom', 'c_1', 'c_2', 'c_3', 'alfa_e']
    # Create plot figure
    #     fig = plt.figure()
    #     plt.subplot(131)
    #     plt.plot(np.cumsum(elastic[::-1])[::-1],-lf.depth,color = 'r')
    #     plt.plot(np.cumsum((creep +elastic)[::-1])[::-1],-lf.depth,color = 'orange')
    #     plt.plot(settlement[::-1],-lf.depth,color = 'green')
    #     plt.subplot(132)
    #     plt.plot(settlement[::-1], -lf.depth)
    #     plt.subplot(133)
    #     plt.plot(iz,-lf.depth, color = 'r')
    # Log output
    if verbose:
        log("delta_p:", delta_p)
        log("c_1:", c_1)
        log("c_2:", c_2)
        log("c_3:", c_3)
        log("zp:", zp)
        log("z_top:", z_top)
        log("z_bottom:", z_bottom)
        log("overburden / sigma_v1_eff:", overburden)
        log("delta_p:", delta_p)
        log("i_zp:", i_zp)
        log("iz", max(iz))
        log("settlement:", settlement[-1], settlement[0], max(settlement))
        log("result: ", result)
    return dict(zip(cols, args))
