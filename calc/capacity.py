import numpy as np
import liquepy as lq

from miscellaneous import log, timed
from foundations import foundation

UNIT_WATER = 10


# TODO: Circular foundation ? fd.short/long , beff - leff?
# TODO: Future -> add loads to foundation object


def calc_shape_factors(fd, phi, nq, nc, b_eff, l_eff, method):
    if method == 'hansen':
        sc = np.where(phi == 0, 0, np.where(fd.shape == 'strip', 1, 1 + (nq * b_eff) / (nc * l_eff)))

        # if phi == 0:
        #     sc = 0.2 * b_eff / l_eff
        # elif fd.shape == "strip":
        #     sc = 1
        # else:
        #     sc = 1 + (nq * b_eff) / (nc * l_eff)
        sq = 1 + (b_eff / l_eff) * np.sin(np.radians(phi))  # Hansen
        sy = np.where(1 - 0.4 * b_eff / l_eff < 0.6, 0.6, 1 - 0.4 * b_eff / l_eff)  # limit to 0.6
        return sc, sq, sy

    elif method == 'vezic':
        if fd.shape == "strip":
            sc = 1
        else:
            sc = 1 + (nq * fd.short) / (nc * fd.long)

        sq = 1 + (fd.short / fd.long) * np.tan(np.radians(phi))  # Vezic
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
        k = np.arctan(fd.depth / fd.short)

    dc = np.where(method == 'hansen' and phi == 0, 0.4 * k, 1 + 0.4 * k)
    # if method == 'hansen' and phi == 0:
    #     dc = 0.4 * k
    # else:
    #     dc = 1 + 0.4 * k
    dq = 1 + (2 * np.tan(np.radians(phi)) * (1 - np.sin(np.radians(phi))) ** 2) * k
    dy = 1

    return dc, dq, dy


def calc_ground_factors(phi, beta, iq, method):
    """
    Returns ground factors
    """

    # Ground factors
    if method == 'hansen':
        gc = np.where(phi == 0, beta / 147, 1 - beta / 147)
        # if phi == 0:
        #     gc = beta / 147
        # else:
        #     gc = 1 - beta / 147
        gq = gy = (1 - 0.5 * np.tan(np.radians(beta))) ** 5
        return gc, gq, gy

    elif method == 'vezic':
        gc = np.where(phi == 0, beta / 5.14, iq - (1 - iq) / (5.14 * np.tan(np.radians(phi))))
        # if phi == 0:
        #     gc = beta / 5.14
        # else:
        #     gc = iq - (1 - iq) / (5.14 * np.tan(np.radians(phi)))

        gq = gy = (1 - np.tan(np.radians(beta))) ** 2
        return gc, gq, gy


def calc_base_factors(phi, beta, eta, gc, method):
    """
    Returns base factors
    """
    # Method by Hansen
    if method == 'hansen':
        bc = np.where(phi == 0, eta / 147, 1 - eta / 147)
        # if phi == 0:
        #     bc = eta / 147
        # else:
        #     bc = 1 - eta / 147

        bq = np.exp(-2 * eta * np.tan(np.radians(phi)))
        by = np.exp(-2.7 * eta * np.tan(np.radians(phi)))
        return bc, bq, by
    # Method by Vezic
    elif method == 'vezic':
        bc = np.where(phi == 0, gc, 1 - (2 * np.radians(beta)) / (5.14 * np.tan(np.radians(phi))))
        # if phi == 0:
        #     bc = gc
        # else:
        #     bc = 1 - (2 * np.radians(beta)) / (5.14 * np.tan(np.radians(phi)))

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
    q_tn_cs = np.abs(lf.big_q * k_c)
    # _phi = 33 + 15.84 * np.log10(q_tn_cs) - 26.88
    _phi = np.nan_to_num(33 + 15.84 * np.log10(q_tn_cs) - 26.88, nan=33)

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


def calc_unit_wt_eff_cpt(fd, lf, gwl):
    unit_wt = np.average(lf.unit_wt[lf.depth <= fd.short])
    if gwl <= fd.depth:
        return unit_wt - UNIT_WATER

    elif 0 < gwl < fd.short:
        return 1 / fd.short * (unit_wt * gwl + (unit_wt - UNIT_WATER) * (fd.short - gwl))
    else:
        return unit_wt


def calc_unit_wt_eff(fd, gwl, gamma_dry, gamma_sat, gamma_water):
    if gwl <= fd.depth:
        return gamma_sat - gamma_water

    elif 0 < gwl < fd.short:
        return 1 / fd.short * (gamma_dry * gwl + (gamma_sat - gamma_water) * (fd.short - gwl))
    else:
        return gamma_dry


def calc_inclination_factors(fd, area, phi, cohesion, nc, nq, h_short, h_long, vload, method):
    """
    Returns what
    """
    ## Inclination factors
    hi = max(h_long, h_short)  # Horizontal h_long or h_short
    if cohesion == 0:
        base_cohesion = 0.6 * 1e-6  # Solve division by 0
    else:
        base_cohesion = 0.6 * cohesion

    if method == 'hansen':

        alfa_1 = alfa_2 = 2  # Use alfa factor of 2

        iq = (1 - (0.5 * hi * fd.long / (
                    vload * fd.long + area * base_cohesion * 1 / np.tan(np.radians(phi))))) ** alfa_1

        ic = np.where(phi == 0, 0.5 - np.sqrt(1 - hi * fd.long / (area * base_cohesion)), iq - (1 - iq) / (nq - 1))
        # if phi == 0:
        #     ic = 0.5 - np.sqrt(1 - hi / (area * base_cohesion))
        # else:
        #     ic = iq - (1 - iq) / (nq - 1)

        iy = (1 - 0.7 * hi * fd.long / (vload * fd.long + area * base_cohesion * 1 / np.tan(np.radians(phi)))) ** alfa_2

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
        iq = (1 - hi * fd.long / (vload * fd.long + area * base_cohesion * 1 / np.tan(np.radians(phi)))) ** m

        # ic
        ic = np.where(phi == 0, 1 - (m * hi * fd.long) / (area * base_cohesion * nc), iq - (1 - iq) / (nq - 1))
        # if phi == 0:
        #     ic = 1 - (m * hi) / (area * base_cohesion * nc)
        # else:
        #     ic = iq - (1 - iq) / (nq - 1)

        iy = (1 - hi * fd.long / (vload * fd.long + area * base_cohesion * 1 / np.tan(np.radians(phi)))) ** (m + 1)

        return ic, iq, iy


@timed.timed
def bearing_capacity(lf, fd, vload=1, gwl=None, **kwargs):
    """
    Returns bearing capacity function.
    Defaults to hansen

    """

    # Loading properties

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
    gamma_water = kwargs.get('gamma_water', 10)

    # Method
    method = kwargs.get('method', 'hansen')
    verbose = kwargs.get('verbose', True)

    if fd.shape == 'circular':
        load = vload / (fd.radius ** 2 * np.pi)
    else:
        load = vload * fd.long / (fd.short * fd.long)

    # if lf and phi.all():
    #     raise ValueError("You cannot both CPT object and define your own friction angle")

    if method not in ['hansen', 'vezic']:
        raise NotImplemented(
            f"{method} Not implemented.You can only choose between hansen or vezic method")
    if (h_long or h_short) and not load:
        raise ValueError("You need to specify the design load ")

    if fd.shape == 'circular':
        raise NotImplemented('Circular footings are not yet implemented for BC equations')

    if gwl is None and lf.gwl is not None:
        gwl = lf.gwl

    if phi is None:  # allow manual input of bearing capacity soil param.
        phis = calc_phi(lf)
        phi = np.average(phis[lf.depth <= fd.short])
        # phi = np.average(phi[lf.depth <= fd.short])  # To check influence depth of the bearing capacity
        # unit_weight_eff = np.average(lf.unit_wt[lf.depth <= fd.short])
        # unit_weight_eff = gamma_dry + 1
        unit_weight_eff = calc_unit_wt_eff_cpt(fd, lf, gwl)
    else:
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

    bc_dict = {
        # "Phi": phi,
        "Unit_eff": unit_weight_eff,
        "Foundation": f"{fd.short}x{fd.long}x{fd.depth}",
        "Nc,Nq,Ny": (np.round(nc, 2), np.round(nq, 2), np.round(ny, 2)),
        "sc,sq,sy": (np.round(sc, 2), np.round(sq, 2), np.round(sy, 2)),
        "dc,dq,dy": (dc, dq, dy),
         "ic,iq,iy": (ic, iq, iy),
        "gc,gq,gy": (gc, gq, gy),
        "bc,bq,by": (bc, bq, by),
        "terms": (np.round(first_term, 2), np.round(second_term, 2), np.round(third_term, 2)),
        "q_ult": np.round((q_ult), 2),
        "q_safe": np.round((q_ult / 2), 2),
        "load": load,
        "FoS": np.round(q_ult / load, 2),
        "method": method
    }
    if verbose:
        print(fd)
        log.log("Friction angle is: ", np.round(phi))
        log.log("Calculates the bearing capacity based on Vesic equations:")
        log.log(f"Shape factors: sc, sq, sy:", np.round(sc, 2), np.round(sq, 2), np.round(sy, 2))
        log.log(f"Depth factors dc, dq, dy:", dc, dq, dy)
        log.log(f"Inclination factor ic, iq, iy:", ic, iq, iy)
        log.log(f"Ground factors gc, gq, gy:", gc, gq, gy)
        log.log(f"Base factors bc, bq, by", bc, bq, by)
        log.log(f"Effective unit weight:", f"{np.round(unit_weight_eff, 2)}")
        log.log(f"Nc,Nq,Ny are:", np.round(nc, 2), np.round(nq, 2), np.round(ny, 2))
        log.log(f"1st,2nd,3rd term:", np.round(first_term, 2), np.round(second_term, 2), np.round(third_term, 2))
        log.log("Surcharge is:", f"{surcharge}kPa")
        log.log(f"Ultimate bearing capacity is:", np.round(q_ult, 2))
        log.log(f"Net allowable bearing capacity is:", np.round(q_ult, 2) / 2)
        log.log(f"Design pressure is:", f"{(load)}kPa < {np.round(q_ult, 2) / 2}kpa")
        log.log(f"Factor of safety is : {np.round(q_ult / load, 2)}")
    return bc_dict


#
phiss = np.array([5, 5, 10, 15, 20, 25, 26, 28, 30])
phis = np.array([30, 36])
fd = foundation.FoundationObject(1, 2, 1)
cpt = lq.field.load_mpa_cpt_file("CPT_H15c.csv", delimiter=";")
lf = lq.trigger.run_bi2014(cpt, pga=0.25, m_w=7.5)

# aa = bearing_capacity(lf=lf, fd=fd)
# bb = bearing_capacity(lf=lf, fd=fd, method = 'vezic', gwl = 3)

cc = bearing_capacity(lf=None, fd=fd, method='vezic', gwl=3, phi=phis,
                      cohesion=250, gamma_dry=20, gamma_sat=20, h_short=1255, vload=7188,
                      verbose=True)

print(cc)
