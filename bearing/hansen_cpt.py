import numpy as np
import liquepy as lq
from numpy import testing
from fig import log
from foundations import foundation


# TODO: Add keyword argument to calculate either for vezic / hansen?
# TODO: REVAMP THE 3 LOAD CASES WITH GAMMA
# TODO: CHECK ALL BEARING, ANGLES AND WHAT ELSE
# TODO: What happens if you have fine soils?
# TODO: FUTURE BEARING, PERHAPS A NICE VISUALIZATION.
# TODO: SOLVE INNFINITY ERROR, how to handle
# TODO: INTERESTING IDEA. LOADS ARE COMING FROM THE FOUNDATION OR FROM BEARING?
# TODO: How do you solve to check beraing if LF object is not introduced?
# TODO: Circular foundation ? fd.short/long , beff - leff?
# TODO: Future -> add loads to foundation object
# TODO: SOLVE nan
# TODO: Solve negative depth factors when gwl < 0 & fd.depth > 0. Even when gwl >0 but when a normal layer is passed as argument
# TODO: Wrap results in a dict
def calc_shape_factors(fd, phi, nq, nc, b_eff, l_eff, method):
    if method == 'hansen':
        if phi == 0:
            sc = 0.2 * b_eff / l_eff
        elif fd.shape == "strip":
            sc = 1
        else:
            sc = 1 + (nq * b_eff) / (nc * l_eff)
        sq = 1 + (b_eff / l_eff) * np.sin(np.radians(phi))  # Hansen
        sy = np.where(1 - 0.4 * b_eff / l_eff < 0.6, 0.6, 1 - 0.4 * b_eff / l_eff)  # limit to 0.6
        return sc, sq, sy

    elif method == 'vezic':
        if fd.shape == "strip":
            sc = 1
        else:
            sc = 1 + (nq * fd.short) / (nc * fd.long)

        sq = 1 + (fd.short / fd.long) * np.tan(np.radians(phi))  # Hansen
        sy = np.where(1 - 0.4 * fd.short / fd.long <= 0.6, 0.6, 1 - 0.4 * fd.short / fd.long)
        return sc, sq, sy
    else:
        pass


def calc_depth_factors(fd, phi, method):
    """"
    Return depth factors
    """
    # Depth factors

    if fd.depth / fd.short <= 1:
        k = fd.depth / fd.short
    else:
        k = np.tan(fd.depth / fd.long) ** -1

    if method == 'hansen' and phi == 0:
        dc = 0.4 * k
    else:
        dc = 1 + 0.4 * k
    dq = 1 + (2 * np.tan(np.radians(phi)) * (1 - np.sin(np.radians(phi))) ** 2) * k
    dy = 1

    return dc, dq, dy


def calc_inclination_factors(fd, area, phi, cohesion, nc, nq, h_short, h_long, vload, method):
    """
    Returns what
    """
    ## Inclination factors
    hi = max(h_long, h_short)  # Horizontal h_long or h_short
    base_cohesion = 0.6 * cohesion

    if method == 'hansen':

        alfa_1 = alfa_2 = 2  # Use alfa factor of 2

        iq = (1 - (0.5 * hi / (vload + area * base_cohesion * 1 / np.tan(np.radians(phi))))) ** alfa_1

        if phi == 0:
            ic = 0.5 - np.sqrt(1 - hi / (area * base_cohesion))
        else:
            ic = iq - (1 - iq) / (nq - 1)

        iy = (1 - 0.7 * hi / (vload + area * base_cohesion * 1 / np.tan(np.radians(phi)))) ** alfa_2

        return ic, iq, iy

    elif method == 'vezic':

        ml = (2 + fd.long / fd.short) / (1 + fd.long / fd.short)
        mb = (2 + fd.short / fd.long) / (1 + fd.short / fd.long)

        if h_long == 0 or h_short == 0:  # Will only return true if h_long and h_short are != than zero #needs testing
            if h_long != 0:
                m = ml
            if h_short != 0:
                m = mb
        if h_long != 0 and h_short != 0:
            m = np.sqrt(ml ** 2 + mb ** 2)

        if h_long == 0 and h_short == 0:
            m = 1

        # Inclination factors
        iq = (1 - hi / (vload + area * base_cohesion * 1 / np.tan(np.radians(phi)))) ** m

        # ic
        if phi == 0:
            ic = 1 - (m * hi) / (area * base_cohesion * nc)
        else:
            ic = iq - (1 - iq) / (nq - 1)

        iy = (1 - hi / (vload + area * base_cohesion * 1 / np.tan(np.radians(phi)))) ** (m + 1)

        return ic, iq, iy


def calc_ground_factors(phi, beta, iq, method):
    """
    Returns ground factors
    """

    # Ground factors
    if method == 'hansen':
        if phi == 0:
            gc = beta / 147
        else:
            gc = 1 - beta / 147
        gq = gy = (1 - 0.5 * np.tan(np.radians(beta))) ** 5
        return gc, gq, gy

    elif method == 'vezic':
        if phi == 0:
            gc = beta / 5.14
        else:
            gc = iq - (1 - iq) / (5.14 * np.tan(np.radians(phi)))

        gq = gy = (1 - np.tan(np.radians(beta))) ** 2
        return gc, gq, gy


def calc_base_factors(phi, beta, eta, gc, method):
    """
    Returns base factors
    """
    # Method by Hansen
    if method == 'hansen':
        if phi == 0:
            bc = eta / 147
        else:
            bc = 1 - eta / 147

        bq = np.exp(-2 * eta * np.tan(np.radians(phi)))
        by = np.exp(-2.7 * eta * np.tan(np.radians(phi)))
        return bc, bq, by
    # Method by Vezic
    elif method == 'vezic':
        if phi == 0:
            bc = gc
        else:
            bc = 1 - (2 * np.radians(beta)) / (5.14 * np.tan(np.radians(phi)))

        bq = by = (1 - np.radians(eta) * np.tan(np.radians(phi))) ** 2
        return bc, bq, by


def calc_nc_nq_nc(phi, method):
    """
    Returns a tuple containing (Nc, Nq, Ny)
   
    """
    nq = np.exp(np.pi * np.tan(np.radians(phi))) * np.power(np.tan(np.radians(45 + phi / 2)), 2)  # checked
    nc = np.where(phi == 0, 5.14, (nq - 1) * (1 / np.tan(np.radians(phi))))  # Solve infinity issue
    if method == 'hansen':
        ny = 1.5 * (nq - 1) * np.tan(np.radians(phi))  # Hansen
    elif method == 'vezic':
        ny = 2 * (nq + 1) * np.tan(np.radians(phi))  # Hansen

    return nc, nq, ny


def calc_surcharge(fd, gamma_fill):
    if fd.depth > 0:
        return gamma_fill * fd.depth
    else:
        return 0


def calc_phi(lf):
    """
    Returns friction angle array based on Jefferies and Been (2006)
    """
    k_c = np.where(lf.i_c <= 1.64, 1,
                   5.581 * lf.i_c ** 3 - 0.403 * lf.i_c ** 4 - 21.63 * lf.i_c ** 2 + 33.75 * lf.i_c - 17.88)
    q_tn_cs = lf.big_q * k_c
    _phi = 33 + 15.84 * np.log10(q_tn_cs) - 26.88
    _phi = np.nan_to_num(_phi, nan=33)

    return np.where(_phi > 45, 45, _phi)


def calc_eff_b_l(fd, med_short, med_long, vload):
    if med_short == 0 & med_long == 0:  # This needs testing
        return fd.short, fd.long
    else:
        eb = med_short / vload
        el = med_long / vload
        b_eff = fd.short - 2 * eb
        l_eff = fd.long - 2 * el

    return b_eff, l_eff


def calc_unit_wt_eff(fd, gwl, gamma_dry, gamma_sat, gamma_water):
    if gwl <= fd.depth:
        return gamma_sat - gamma_water

    elif 0 < gwl < fd.short:
        return 1 / fd.short * (gamma_dry * gwl + (gamma_sat - gamma_water) * (fd.short - gwl))
    else:
        return gamma_dry


def bearing_capacity(lf, fd, load=0, gwl=None, **kwargs):
    """
    Returns bearing capacity function

    """

    # Loading properties
    vload = kwargs.get('vload', 1)
    h_short = kwargs.get('h_short', 0)
    h_long = kwargs.get('h_long', 0)
    med_short = kwargs.get('med_short', 0)
    med_long = kwargs.get('med_long', 0)

    # Geometry Proprieties
    beta = kwargs.get('beta', 0)
    eta = kwargs.get('eta', 0)

    # Soil Proprieties
    phi = kwargs.get('phi', None)
    cohesion = kwargs.get('cohesion', 0)
    gamma_dry = kwargs.get('gamma_dry', None)
    gamma_sat = kwargs.get('gamma_sat', None)
    gamma_fill = kwargs.get('gamma_fill', 17)
    gamma_water = kwargs.get('gamma_water', 10.25)

    # Method
    method = kwargs.get('method', 'hansen')

    if method not in ['hansen', 'vezic']:
        raise NotImplemented(
            f"{method} Not implemented.You can only choose between hansen or vezicmethod")

    if gwl is None and lf.gwl is not None:
        gwl = lf.gwl

    if phi is None:  # allow for manual input of phi? Otherwise we can calculate for phi.
        phis = calc_phi(lf)
        phi = np.average(phis[lf.depth <= fd.short])
        # phi = np.average(phi[lf.depth <= fd.short])  # To check influence depth of the bearing capacity
        gamma_dry = np.average(lf.unit_wt[lf.depth <= fd.short])
        gamma_sat = gamma_dry + 1

    unit_weight_eff = calc_unit_wt_eff(fd, gwl, gamma_dry, gamma_sat, gamma_water)
    surcharge = calc_surcharge(fd, gamma_fill)

    nc, nq, ny = calc_nc_nq_nc(phi, method)
    b_eff, l_eff = calc_eff_b_l(fd, med_short, med_long, vload)

    area = b_eff * l_eff
    sc, sq, sy = calc_shape_factors(fd, phi, nq, nc, b_eff, l_eff, method)
    dc, dq, dy = calc_depth_factors(fd, phi, method)

    ic, iq, iy = calc_inclination_factors(fd, area, phi, cohesion, nc, nq, h_short, h_long, vload, method)
    gc, gq, gy = calc_ground_factors(phi, beta, iq, method)
    bc, bq, by = calc_base_factors(phi, beta, eta, gc, method)

    first_term = cohesion * nc * sc * dc * ic * gc * bc
    second_term = surcharge * nq * sq * dq * iq * gq * bq
    third_term = 0.5 * unit_weight_eff * b_eff * ny * sy * dy * iy * gy * by

    q_ult = first_term + second_term + third_term
    log.log("Friction angle is: ", phi)
    log.log("Calculates the bearing capacity based on Vesic equations:")
    log.log(f"Shape factors: sc, sq, sy:", sc, sq, sy)
    log.log(f"Depth factors dc, dq, dy:", dc, dq, dy)
    log.log(f"Inclination factor ic, iq, iy:", ic, iq, iy)
    log.log(f"Ground factors gc, gq, gy:", gc, gq, gy)
    log.log(f"Base factors bc, bq, by", bc, bq, by)
    log.log(f"Effective unit weight:", f"{unit_weight_eff:.2f}")
    log.log(f"Nc,Nq,Ny are:", nc, nq, ny)
    log.log(f"1st,2nd,3rd term:", f"{first_term:.2f}", f"{second_term:.2f}", f"{third_term:.2f}")
    log.log("Surcharge is:", f"{surcharge}kPa")
    log.log(f"Ultimate bearing capacity is:", f"{q_ult:.2f}kPa")
    log.log(f"Net allowable bearing capacity is:", f"{q_ult / 2:.2f}kPa")
    log.log(f"Design pressure is:", f"{(load / (fd.short * fd.long)):.2f}kPa < {q_ult / 2:.2f}kpa")


# phiss = np.array([0, 5, 10, 15, 20, 25, 26, 28, 30, 32, 34, 36, 38, 40, 45, 50])
# nc, nq, ny = calc_nc_nq_nc(phiss, 'hansen')

# from tests import values
#
# n_y_hansen_test = np.array([0, 0.1, 0.4, 1.2, 2.9, 6.8, 7.9, 10.9, 15.1, 20.8, 28.7, 40.0, 56.1, 79.4, 200.5, 567.4])
#
# testing.assert_allclose(nc, values.n_c_test, rtol=0.1)
# # testing.assert_allclose(nq, values.n_q_test, rtol=0.1)
# # testing.assert_allclose(ny, n_y_hansen_test, rtol=0.1)
# #

# for phi, _, __, ___ in zip(phiss, nc, nq, ny, ):
#     print(f"{phi},{_:.2f},{__:.2f},{___:.2f}")

fd = foundation.FoundationObject(1, 1, 3)
# cpt = lq.field.load_mpa_cpt_file("CPT_H15c.csv", delimiter=";")
# bf, sps = plt.subplots(ncols=3, sharey=True, figsize=(8, 6))
# print(cpt.file_name)

# lf = lq.trigger.run_bi2014(cpt, pga=0.25, m_w=7.5, gwl=-1)

# bearing_capacity(lf,fd)
bearing_capacity(lf=None, fd=fd, phi=30, gwl=3, gamma_dry=18, gamma_sat=19, method='vezic')
