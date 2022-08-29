from math import *

# TODO Implement undrained shear strength calculations
# TODO Test inclination, and ground factors scenarios
# TODO Implement/Activate Moment, Horizontal load
# TODO Do eccentricity check
# TODO fix surcharge,ubc value when  we have  water table above ground level. It yields negative value otherwise. In other words, it desnt work for underwaters structyures
# TODO
# Constants

y_water = 10
med_b = 0
med_l = 0
v = 1
hb = 0
hl = 0
beta = 0
eta = 0


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


def bearingVesic(L, B, df, gwl, gl, y_dry, y_sat, phi, c=0, dload=0,f_type='rectangular') -> float:
    """
    Returns the ultimate bearing capacity  based on Vesic Equations
    :param L: length
    :param B: width (It doesn't matter how you introduce them, we take width = min(l,b)
    :param df: Foundation Depth
    :param gwl: Ground water level mASL
    :param gl: Ground level mASL
    :param y_dry: Gamma dry
    :param y_sat: Gamma sat
    :param phi: Friction Angle
    :param c:  Cohesion
    :param dload: Load on foundation
    :param f_type: Rectangular / Mat
    :return:
    """

    l, b = max(L, B), min(L, B)  # Swap l,b for min value regarding width

    if l / b < 10:
        f_type = "rectangular"
    else:
        f_type = "strip"

    fl = gl - df  # foundation level in meters relative to the sea level

    y_avg, q_over = gamma_average_surcharge(gwl, df, fl, y_dry, y_sat, b)  # Retrieve overburden pressure and y_average

    # nc, nq, ny
    nq = exp(pi * tan(radians(phi))) * pow(tan(radians(45 + phi / 2)), 2)  # checked
    nc = (nq - 1) * (1 / tan(radians(phi)))
    #ny = 2 * (nq + 1) * tan(radians(phi))  # Vesic
    ny = (nq-1)*tan(radians(1.4*phi)) #Hansen

    # Shape factors
    if f_type == "strip":
        sc = 1
    else:
        sc = 1 + (nq * b) / (nc * l)

    sq = 1 + b * tan(radians(phi)) / l  # Vesic

    _sy = 1 - 0.4 * b / l
    if _sy < 0.6:
        sy = 0.6
    else:
        sy = _sy

    # Depth factors
    if df / b <= 1:
        k = df / b
    else:
        k = atan(df / b)

    dc = 1 + 0.4 * k
    dq = 1 + 2 * tan(radians(phi)) * (1 - sin(radians(phi))) ** 2 * k
    dy = 1

    ## Inclination factors

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
    iq = (1 - (hi) / (v + area * 0.6 * c * 1 / tan(radians(phi)))) ** m

    # ic
    if phi == 0:
        ic = 1 - (m * hi) / (area * 0.6 * c * nc)

    else:
        ic = iq - (1 - iq) / (nq - 1)

    iy = (1 - hi / (v + area * 0.6 * c * 1 / tan(radians(phi)))) ** (m + 1)

    # Ground factors
    if phi == 0:
        gc = beta / 5.14
    else:
        gc = iq - (1 - iq) / (5.14 * tan(radians(phi)))

    gq = gy = (1 - tan(radians(beta))) ** 2

    # Base factors (Tilted base)

    if phi == 0:
        bc = gc
    else:
        bc = 1 - (2 * radians(beta)) / (5.14 * tan(radians(phi)))

    bq = by = (1 - radians(eta) * tan(radians(phi))) ** 2

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
    print(f"Eccentricity is {eb}, ratio of e/b is {eb/b}")




    print(f"1st,2nd,3rd term: {c * nc * sc * dc * ic * gc * bc:.2f},"
          f"{q_over * nq * sq * dq * iq * gq * bq:.2f},"
          f"{0.5 * y_avg * b_eff * ny * sy * dy * iy * gy * by:.2f}")
    print(f"{b}mx{l}m,{df},{y_avg:.2f},{q_ult:.2f}, --- {f_type}")
    print()
    print(f"Ultimate bearing capacity is: {q_ult:.2f}kPa")
    print(f"Net allowable bearing capacity is {q_ult/2:.2f}kPa")
    print(f"Design pressure is {dload/(b*l):.2f}kPa < {q_ult/2:.2f}kpa")

    wxl = f"{b}mx{l}m"

    #return wxl,df,y_avg,q_ult,f_type

#bearingVesic(L, B, df, gwl, gl, y_dry, y_sat, phi, c=0)
#bearingVesic(1.2, 1.2, 0,0,0, 20, 21, 40,0,301.297) #For Node 6
bearingVesic(0.9, 0.9, 0,0,0, 20, 21, 40,0,128.293) #For Node 9
