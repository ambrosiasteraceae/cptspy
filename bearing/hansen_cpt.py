import numpy as np
from math import *
from numpy import testing


# TODO: Add keyword argument to calculate either for vezic / hansen?
# TODO: REVAMP THE 3 LOAD CASES WITH GAMMA
# TODO: CHECK ALL BEARING, ANGLES AND WHAT ELSE
# TODO: What happens if you have fine soils?
# TODO: FUTURE BEARING, PERHAPS A NICE VISUALIZATION.
# TODO: SOLVE INNFINITY ERROR, how to handle
# TODO: INTERESTING IDEA. LOADS ARE COMING FROM THE FOUNDATION OR FROM BEARING?

def gamma_average_surcharge(gwl, df, fl, y_dry, y_sat, b) -> tuple:
    """
      Calculates the water condition and returns an averaged gamma and the surcharge pressure
    :return:
    """
    # Case I if the GWl is higher than the foundation depth. This is similar to submerged

    fl = gl - df  # foundation level in meters relative to the sea level
    
    fl = fd.depth
    
    gwl > fd.depth
    
    waterdepth = gwl - fd.depth
    

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



def calc_bxleff(fd,med_short,med_long,vload):
    """"
    ADSA
    """
    if med_short == 0 & med_long == 0:  # This needs testing
        return fd.short, fd.long
    else:
        eb = med_short / vload
        el = med_long / vload
        b_eff = fd.short - 2 * eb
        l_eff = fd.long - 2 * el
        area = b_eff * l_eff
        return b_eff, l_eff

 def calc_shape_factors(fd,b_eff,l_eff):

    if fd.shape == "strip":
        sc = 1
    else:
        sc = 1 + (nq * b_eff) / (nc * l_eff)
    
    sq = 1 + (b_eff / l_eff) * np.tan(np.radians(phi))  # Hansen
    
    _sy = 1 - 0.4 * b_eff / l_eff
    
    if _sy < 0.6:
        sy = 0.6
    else:
        sy = _sy
        
    return None

def calc_depth_factors(fd,phi):
    """"
    Return depth factors
    """
     #Depth factors
    if fd.depth / fd.short <= 1:
        k = fd.depth / fd.short
    else:
        k = np.tan(fd.depth / fd.long)
    dc = 1 + 0.4 * k
    dq = 1 + 2 * np.tan(np.radians(phi)) * (1 - sin(np.radians(phi))) ** 2 * k
    dy = 1
    
    return dc,dq,dy



def calc_inclination_factors(fd, area, phi, cohesion, h_short,h_long,vload):
    """
    Returns what
    """
    ## Inclination factors

    ml = (2 + fd.long / fd.short) / (1 + fd.long / fd.short)
    mb = (2 + fd.short / fd.long) / (1 + fd.short / fd.long)

    if h_long == 0 or h_short == 0:  # Will only return true if h_long and h_short are != than zero #This also needs testing
        if h_long != 0:
            m = ml
        if h_short != 0:
            m = mb
    if h_long != 0 and h_short != 0:
        m = sqrt(ml ** 2 + mb ** 2)

    if h_long == 0 and h_short == 0:
        m = 1

    hi = max(h_long, h_short)  # Horizontal h_long or h_short

    # Inclination factors
    iq = (1 - hi / (vload + area * 0.6 * cohesion * 1 / np.tan(np.radians(phi)))) ** m

    # ic
    if phi == 0:
        ic = 1 - (m * hi) / (area * 0.6 * cohesion * nc)
    else:
        ic = iq - (1 - iq) / (nq - 1)

    iy = (1 - hi / (vload + area * 0.6 * cohesion * 1 / np.tan(np.radians(phi)))) ** (m + 1)

    return ic,iq,iy



def calc_ground_factors(phi,beta,iq):
    """
    Returns ground factors
    """

    # Ground factors
    if phi == 0:
        gc = beta / 5.14
    else:
        gc = iq - (1 - iq) / (5.14 * np.tan(np.radians(phi)))

    gq = gy = (1 - np.tan(np.radians(beta))) ** 2

    return None


def calc_base_factors(phi,beta,eta,gc):
    """
    Returns base factors
    """

    # Base factors (Tilted base)

    if phi == 0:
        bc = gc
    else:
        bc = 1 - (2 * np.radians(beta)) / (5.14 * np.tan(np.radians(phi)))

    bq = by = (1 - np.radians(eta) * np.tan(np.radians(phi))) ** 2

    return None


def calc_nc_nq_nc(phi):
    """
    Returns a tuple containing (Nc, Nq, Ny)
   
    """

    nq = np.exp(np.pi * np.tan(np.radians(phi))) * np.power(np.tan(np.radians(45 + phi / 2)), 2)  # checked
    nc = np.where(phi == 0,0,(nq - 1) * (1 / np.tan(np.radians(phi)))) #Solve infinity issue
    ny = 1.5 * (nq - 1) * np.tan(np.radians(phi))  # Hansen

    return nc, nq, ny


def calc_unit_wt():

    """
    Work  in progress

    """
    pass


def calc_surcharge(fd,gamma_fill):

    if fd.depth > 0:
        return gamma_fill * fd.depth
    else:
        return 0

def calc_bearing_case(fd,gwl):
    """
    Returns the three cases to account for water pressure
    """
    if fd.depth > gwl:
        pass
    elif fd.depth == gwl:
        pass
    else:
        pass

    pass

    gammaweught = {'I': fd.depth * gwl,
                   'II': "",
                   'III': ""
                   }


def bearing_hansen(lf, fd, load=None, gwl=None, **kwargs):
    """
    Returns bearing capacity function

    """

    #Loading properties
    vload = kwargs.get('vload', 1)
    h_short = kwargs.get('h_short', 0)
    h_long = kwargs.get('h_long', 0)
    med_short = kwargs.get('med_short', 0)
    med_long = kwargs.get('med_long', 0)

    #Geometry Proprieties
    beta = kwargs.get('beta', 0)
    eta = kwargs.get('eta', 0)

    #Soil Proprieties
    phi = kwargs.get('phi', None)
    cohesion = kwargs.get('cohesion', None)
    gamma_dry = kwargs.get('gamma_dry', None)
    gamma_sat = kwargs.get('gamma_sat', None)
    gamma_fill = kwargs.get('gamma_fill', None)
    


    if gwl is None and lf.gwl is not None:
        gwl = lf.gwl

    if phi is None:  # allow for manual input of phi? Otherwise we can calculate for phi.
        phi = np.average(lf.phi[lf.depth <= fd.short]) #To check influence depth of the bearing capaccity
        unit_weight_eff = np.average(lf.unit_wt[lf.depth<=fd.short])

    else:
        unit_weight_eff = calc_unit_wt(fd, gwl, gamma_dry)
        phi = phi


    

    case = calc_bearing_case()
    surcharge = calc_surcharge(fd,lf,gamma_dry,gamma_sat,gamma_fill)
    nc, nq, ny = calc_nc_nq_nc(phi)
    b_eff, l_eff = calc_bxleff(fd,med_short,med_long,vload)
    
    area = b_eff * l_eff
    
    sc, sq, sy = calc_shape_factors(fd,b_eff,l_eff)
    dc,dq,dy = calc_depth_factors(fd,phi)
    ic, iq, iy = calc_inclination_factors(fd, area, phi, cohesion, h_short,h_long,vload)
    gc, gq, gy = calc_ground_factors(phi,beta,iq)
    bc, bq, by = calc_base_factors(phi,beta,gc,)

    first_term =  cohesion * nc * sc * dc * ic * gc * bc
    second_term = surcharge * nq * sq * dq * iq * gq * bq
    third_term = 0.5 * unit_weight_eff * b_eff * ny * sy * dy * iy * gy * by

    q_ult = first_term + second_term + third_term

    print("Calculates the bearing capacity based on Vesic equations: ")

    print(f"Shape factors {sc, sq, sy}")
    print(f"Depth factors {dc, dq, dy}")
    print(f"Inclination factor {ic, iq, iy}")
    print(f"Ground factors {gc, gq, gy}")
    print(f"Base factors {bc, bq, by}")
    print(f"Averaged unit weight is {unit_weight_eff} and the surcharge is {surcharge}")
    print(f"Nc,Nq,Ny are: {nc, nq, ny}")
    print(f"k is {k}")
    print(f"Eccentricity is {eb}, ratio of e/b is {eb / b}")
    print(f"1st,2nd,3rd term: {first_term:.2f},"
          f"{second_term:.2f},"
          f"{third_term:.2f}")
    print(f"{b}mx{l}m,{df},{unit_weight_eff:.2f},{q_ult:.2f}, --- {fd.shape}")
    print()
    print(f"Ultimate bearing capacity is: {q_ult:.2f}kPa")
    print(f"Net allowable bearing capacity is {q_ult / 2:.2f}kPa")
    print(f"Design pressure is {dload / (b * l):.2f}kPa < {q_ult / 2:.2f}kpa")

    wxl = f"{b}mx{l}m"


phis = np.array([0, 5, 10, 15, 20, 25, 26, 28, 30, 32, 34, 36, 38, 40, 45, 50])
nc, nq, ny = calc_nc_nq_nc(phis)

from tests import values
n_y_hansen_test = np.array([0, 0.1, 0.4, 1.2, 2.9, 6.8, 7.9, 10.9, 15.1, 20.8, 28.7, 40.0, 56.1, 79.4, 200.5, 567.4])



#testing.assert_allclose(nc, values.n_c_test, rtol=0.1)
#testing.assert_allclose(nq, values.n_q_test, rtol=0.1)
#testing.assert_allclose(ny, n_y_hansen_test, atol=0.1)

for phi, _, __, ___ in zip(phis, nc, nq, ny):
    print(f"{phi},{_:.2f},{__:.2f},{___:.2f}")

