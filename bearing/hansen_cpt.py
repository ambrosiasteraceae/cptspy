import numpy as np
from math import *
from numpy import testing


# TODO: Add keyword argument to calculate either for vezic / hansen?
# TODO: REVAMP THE 3 LOAD CASES WITH GAMMA
# TODO: CHECK ALL BEARING, ANGLES AND WHAT ELSE
# TODO: What happens if you have fine soils?
# TODO: FUTURE BEARING, PERHAPS A NICE VISUALIZATION.


def gamma_average_surcharge(gwl, df, fl, y_dry, y_sat, b) -> tuple:
    """
      Calculates the water condition and returns an averaged gamma and the overburden pressure
    :return:
    """
    # Case I if the GWl is higher than the foundation depth. This is similar to submerged
    if gwl > fl:

        waterdepth = gwl - fl
        surcharge = y_dry * (df - waterdepth) + (y_sat - y_water) * waterdepth
        if surcharge < 0:
            surcharge = 0
        gamma_ = y_sat - y_water  # Gamma used in the third term of b.c. equation



    # Case II waterdepth @ the same level as foundation level
    elif gwl == fl:

        waterdepth = 0
        surcharge = y_dry * df
        gamma_ = y_sat - y_water


    # Case III water depth below foundation
    else:

        waterdepth = fl - gwl
        surcharge = y_dry * df

        if waterdepth >= b:
            gamma_ = y_dry

        else:
            gamma_ = (1 / b) * (y_dry * waterdepth + (y_sat - y_water) * (b - waterdepth))

    return gamma_, surcharge


# def bearingVesic(L, B, df, gwl, gl, y_dry, y_sat, phi, c=0, dload=0,f_type='recnp.tangular') -> float:




def bearing_hansen(lf, fd, load=None, gwl=None, **kwargs):
    """
    Returns bearing_hansen
    
    """

    vload = kwargs.get('vload', 1)
    h_short = kwargs.get('h_short', 0)
    h_long = kwargs.get('h_long', 0)
    med_short = kwargs.get('med_short', 0)
    med_long = kwargs.get('med_long', 0)
    beta = kwargs.get('beta', 0)
    eta = kwargs.get('eta', 0)
    phi = kwargs.get('phi', 0)
    gamma_dry = kwargs.get('gamma_dry', 0)
    gamma_water = kwargs.get('gamma_water', 10.25)

    if gwl is None and lf.gwl is not None:
        gwl = lf.gwl

    if phi is None:  # allow for manual input of phi? Otherwise we can calculate for phi.
        phi = lf.phi  # If we use numpy perhaps we can iterate for many other types of phi

    # Y_WATER
    #
    # fl = gl - df  # foundation level in meters relative to the sea level
    # y_avg, q_over = gamma_average_surcharge(gwl, df, fl, y_dry, y_sat, b)  # Retrieve overburden pressure and y_average

    nc, nq, ny = calc_nc_nq_nc(phi)

    if med_b == 0 & med_l == 0:  # This needs testing
        area = b * l
        b_eff = b
        l_eff = l
        eb = 0
        el = 0

    else:
        # mb, ml = min(med_b, med_l), max(med_b, med_l)  #Condition not good
        eb = med_b / v
        el = med_l / v
        b_eff = b - 2 * eb
        l_eff = l - 2 * el
        area = b_eff * l_eff

    # Shape factors
    if f_type == "strip":
        sc = 1
    else:
        sc = 1 + (nq * b_eff) / (nc * l_eff)

    sq = 1 + (b_eff / l_eff) * np.tan(np.radians(phi))  # Hansen

    _sy = 1 - 0.4 * b_eff / l_eff

    if _sy < 0.6:
        sy = 0.6
    else:
        sy = _sy

    # Depth factors
    if df / b <= 1:
        k = df / b
    else:
        k = anp.tan(df / b)

    dc = 1 + 0.4 * k
    dq = 1 + 2 * np.tan(np.radians(phi)) * (1 - sin(np.radians(phi))) ** 2 * k
    dy = 1

    ## Inclination factors

    ml = (2 + l / b) / (1 + l / b)
    mb = (2 + b / l) / (1 + b / l)

    if hl == 0 or hb == 0:  # Will only return true if hl and hb are != than zero #This also needs testing
        if hl != 0:
            m = ml
        if hb != 0:
            m = mb
    if hl != 0 and hb != 0:
        m = sqrt(ml ** 2 + mb ** 2)

    if hl == 0 and hb == 0:
        m = 1

    hi = max(hl, hb)  # Horizontal Hl or Hb

    # Inclination factors
    iq = (1 - (hi) / (v + area * 0.6 * c * 1 / np.tan(np.radians(phi)))) ** m

    # ic
    if phi == 0:
        ic = 1 - (m * hi) / (area * 0.6 * c * nc)

    else:
        ic = iq - (1 - iq) / (nq - 1)

    iy = (1 - hi / (v + area * 0.6 * c * 1 / np.tan(np.radians(phi)))) ** (m + 1)

    # Ground factors
    if phi == 0:
        gc = beta / 5.14
    else:
        gc = iq - (1 - iq) / (5.14 * np.tan(np.radians(phi)))

    gq = gy = (1 - np.tan(np.radians(beta))) ** 2

    # Base factors (Tilted base)

    if phi == 0:
        bc = gc
    else:
        bc = 1 - (2 * np.radians(beta)) / (5.14 * np.tan(np.radians(phi)))

    bq = by = (1 - np.radians(eta) * np.tan(np.radians(phi))) ** 2

    q_ult = c * nc * sc * dc * ic * gc * bc + q_over * nq * sq * dq * iq * gq * bq + 0.5 * y_avg * b_eff * ny * sy * dy * iy * gy * by

    print("Calculates the bearing capacity based on Vesic equations: ")

    print(f"Shape factors {sc, sq, sy}")
    print(f"Depth factors {dc, dq, dy}")
    print(f"Inclination factor {ic, iq, iy}")
    print(f"Ground factors {gc, gq, gy}")
    print(f"Base factors {bc, bq, by}")
    print(f"Averaged unit weight is {y_avg} and the surcharge is {q_over}")
    print(f"Nc,Nq,Ny are: {nc, nq, ny}")
    print(f"k is {k}")
    print(f"Eccentricity is {eb}, ratio of e/b is {eb / b}")

    print(f"1st,2nd,3rd term: {c * nc * sc * dc * ic * gc * bc:.2f},"
          f"{q_over * nq * sq * dq * iq * gq * bq:.2f},"
          f"{0.5 * y_avg * b_eff * ny * sy * dy * iy * gy * by:.2f}")
    print(f"{b}mx{l}m,{df},{y_avg:.2f},{q_ult:.2f}, --- {f_type}")
    print()
    print(f"Ultimate bearing capacity is: {q_ult:.2f}kPa")
    print(f"Net allowable bearing capacity is {q_ult / 2:.2f}kPa")
    print(f"Design pressure is {dload / (b * l):.2f}kPa < {q_ult / 2:.2f}kpa")

    wxl = f"{b}mx{l}m"




def calc_nc_nq_nc(phi):
    """
    Returns a tuple containing (Nc, Nq, Ny)
    """
    nq = np.exp(np.pi * np.tan(np.radians(phi))) * np.power(np.tan(np.radians(45 + phi / 2)), 2)  # checked
    nc = np.where(phi == 0,0,(nq - 1) * (1 / np.tan(np.radians(phi)))) #Solve infinity issue
    ny = 1.5 * (nq - 1) * np.tan(np.radians(phi))  # Hansen


    return nc, nq, ny


phis = np.array([0, 5, 10, 15, 20, 25, 26, 28, 30, 32, 34, 36, 38, 40, 45, 50])
nc, nq, ny = calc_nc_nq_nc(phis)

from tests import values
n_y_hansen_test = np.array([0, 0.1, 0.4, 1.2, 2.9, 6.8, 7.9, 10.9, 15.1, 20.8, 28.7, 40.0, 56.1, 79.4, 200.5, 567.4])



#testing.assert_allclose(nc, values.n_c_test, rtol=0.1)
#testing.assert_allclose(nq, values.n_q_test, rtol=0.1)
#testing.assert_allclose(ny, n_y_hansen_test, rtol=0.1)

for phi, _, __, ___ in zip(phis, nc, nq, ny):
    print(f"{phi},{_:.2f},{__:.2f},{___:.2f}")

