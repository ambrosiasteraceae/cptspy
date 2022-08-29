
import os
import glob
import pandas as pd
import liquepy as lq
import matplotlib.pyplot as plt
import timeit
from collections import OrderedDict 
import numpy as np 

#@MAJOR MISMATCH WITH FOUNDATION DEPTH @IZ. 
#DEAL WITH IT
# OK BRO I THINK I DID
#NO YOU DIDINT BRO< YOU FKN DIDNT 22/08/2022
#TODO - Test & Validate Properly
#TODO - Implement interpolation values between L/B [1:10]
#TODO - Implement raft foundatio with Boussinesq
#TODO - Implement soil profiles if rock layers?
#TODO - Implement figures
#TODO - Implement return values
#TODO - Implement creep & consolidation settlements
#TODO - Implement data frame for settlement
#TODO - Implement data frame for liq_obj.attributes / Using Multiindex? No clue
#TODO - Implement bearing capacity
#TODO - Implement elevation function & apply it to depths. Perhaps we dont have to modify the calculations,\
        #just a small artificial thing
#TODO - Implement function to plot & save figure
#TODO - Implement why it doesn't work for consolidation. I have settlement between 1.95 & 2.35 and it shows at -4m... when inverted


class FoundationObject:
    def __init__(self,  length, width, depth = 0 , height = 0, radius = 0):
        self.width = width
        self.length = length
        self.depth = depth
        self.height = height
        self.radius = radius
    def __repr__(self):
        return f'Foundation: W:{self.length}m, L:{self.width}m,\
                    R:{self.radius}, H:{self.height}m, D:{self.depth}m'

def log(out_str, o2="", o3="", o4=""):
    """
    Produces console output.
    :param out_str: Output string
    :param o2: Additional output string
    :param o3: Additional output string
    :param o4: Additional output string
    :return: None
    """
    print(out_str, o2, o3, o4)


def calculate_peak_settlement_indexes(long,short,fdo):
    # Peak settlement index
    #TODO Implement interpolation
    if long / short > 10:
        zp = short + fdo.depth #Absolute Peak elevation of strain influence
        z_top = 0.2 #See figure, first x_value
        z_bottom = 4 * short + fdo.depth  #Elevation where influence becomes 0

    else:
        z_top = 0.1
        zp = 0.5 * short  + fdo.depth
        z_bottom = 2 * short + fdo.depth

    return z_top, z_bottom, zp


def calculate_correction_factors(long,short,overburden, delta, years):
    # EMBEDMENT FACTOR
    c_1 = max(1- 0.5 *(overburden/delta),0.5)
    # CREEP FACTOR
    if years == 0:
        c_2 = 1.0
    else:
        c_2 = 1.0 + 0.2 * np.log10(years / 0.1)

    if long/short > 10:
        c_3 = 1.75
    else:
        c_3 = 1.2
    return c_1, c_2, c_3


def calculate_net_pressure(fdo,sigmas,depths,load):
    #Implement later, an effective stress with certain gamma.
    #Also take note for predrill
    overburden = sigmas[np.where(depths == fdo.depth)] if fdo.depth>0 else 0
    delta_p = load - overburden
    return (delta_p, overburden)
    
    

def calculate_strain_influence_peak (zp,  delta_p, sigmas,depths):
    "Calculate strain_influence_peak"
    mask = np.where(depths == zp) #Index value where depth = zp
    sigma_v1_eff_zp = sigmas[mask] #Effective stress method at peak index at zp 
    i_zp = 0.5 + 0.1 * (delta_p / sigma_v1_eff_zp) ** 0.5 #Strain influence peak
    
    return i_zp

def calculate_iz(fdo,z_top,zp , z_bottom, i_zp, sigmas, depths):
    """
    Calculates the strain influence factor based on line equation
    AB - BC.It starts from the depth of CPT and not at depth of footing.
    """   
    incs = depths[1] - depths[0] 
    limit = depths[-1]

    if z_bottom > limit:
        ll = limit
    else:
        ll = z_bottom
    if fdo.depth == 0 :
        elevs = np.arange(fdo.depth+incs, ll + incs, incs)
    else:
        elevs = np.arange(fdo.depth, ll + incs, incs)
    iz_ab = ((i_zp - 0.1) * (elevs[elevs<=zp] - fdo.depth))/(zp -fdo.depth) + 0.1
    iz_bc = i_zp + (-i_zp*(elevs[np.where(elevs > zp)] - zp))/(z_bottom - zp)
    abbc = np.hstack((iz_ab,iz_bc))

    iz = np.zeros(depths.size)  #Initialize strain_influence
    indexes = np.where((depths>=fdo.depth) & (depths<=ll))
    iz[indexes] = abbc #fancy indexing
    return iz


def calculate_young_modulus(liq_obj):
    """Calculates and returns alfa_e for young modulus coefficient
    """
    _alfa_e = 0.015 * np.power(10,(0.55 * liq_obj.i_c + 1.68))
    alfa_ee = np.where(_alfa_e > 7,7,_alfa_e)
    alfa_bb = np.where((liq_obj.big_q <7) & (liq_obj.big_q > 0) ,liq_obj.big_q,7  )
    alfa_e = np.where(liq_obj.i_c <2.6, alfa_ee, alfa_bb)
    return alfa_e










def calculate_consolidation(alfa_e,liq_obj, incs, i_z,overburden,delta_p):
    """Performs consolidation on the """
    alfa_m = 1.35 * alfa_e #Can this be over 7?
    alfa_m = np.where(alfa_m > 7,7,alfa_m)
    constrained_modulus = alfa_m * (liq_obj.q_t - overburden) 
    e_0 = 0.9 #This is how it is
    c_c = 2.3 * (1 + e_0) * liq_obj.sigma_veff / constrained_modulus
    consolidation = (c_c * incs / (1-e_0)) * np.log10((liq_obj.sigma_veff + i_z * delta_p)/liq_obj.sigma_veff )
    return np.where(liq_obj.i_c>2.6, consolidation,0)




def timed(fn):
    from time import perf_counter
    from functools import wraps 
    @wraps(fn)
    def inner(*args, **kwargs):
        start = perf_counter()
        result = fn(*args, **kwargs)
        end = perf_counter()
        elapsed = end -start         
        print('{} took {:.6f}s  to run'.format(fn.__name__, elapsed))
        return result
    return inner


@timed
def settlement(fdo, liq_obj, load, years, verbose = True, val_limit = 0.025):
    """Calculate settlement based on Schmertmann method
    Inputs:
    fdo - FoundationObject
    liq_obj - LiquepyObject
    load - Load in kPA
    years - No. of years
    verbose - prints to console if True
    
    Outputs:
    sx - ndarray containing cumulative settlement
    """

    long = max(fdo.length, fdo.width)
    short = min(fdo.length, fdo.width)

    sigmas = liq_obj.sigma_veff
    depths = np.round(liq_obj.depth,2)
    incs = depths[1]-depths[0]
    #print(f'Depth of cpt is {depths[-1]}')
    if fdo.depth > depths[-1]:
       raise ValueError("Foundation depth is higher than the depth of the CPT!")

    z_top, z_bottom, zp = calculate_peak_settlement_indexes(long,short,fdo)
    delta_p, overburden = calculate_net_pressure(fdo,sigmas,depths,load)
    c_1, c_2, c_3 = calculate_correction_factors(long,short,overburden, delta_p, years)
    i_zp = calculate_strain_influence_peak(zp,  delta_p, sigmas,depths)
    iz = calculate_iz(fdo,z_top,zp , z_bottom, i_zp, sigmas, depths)
    delta_z = np.ones(depths.size) * incs
    alfa_e = calculate_young_modulus(liq_obj)
   
    #replace with cpt_qc

    if fdo.depth > 0:
        young_modulus = alfa_e * (liq_obj.q_t - overburden)

    else:
        young_modulus = alfa_e * (np.where(liq_obj.q_t <=0.1, np.nan, liq_obj.q_t) - overburden) #q_c is 0 at start, 
     
    #settlement = c_1 * c_2 * delta_p * iz/(c_3*young_modulus)*delta_z

    elastic = (c_1 *  delta_p * iz/(c_3*young_modulus)*delta_z)
    creep = elastic*(c_2 -1)
    consolidation = calculate_consolidation(alfa_e,liq_obj, incs, iz,overburden,delta_p)
    
  
    total = elastic + creep + consolidation
    total = np.cumsum(total[::-1])
    
    
    if max(total[::-1]) > val_limit:
        result = "Value exceeded"
    else:
        result = "Ok"  
    args =[total,elastic,creep,consolidation,iz,overburden,delta_p,i_zp,zp,z_top,z_bottom,c_1,c_2,c_3,alfa_e]
    cols=['settlement','elastic','creep','consolidation','iz','overburden', 
           'delta_p', 'i_zp','zp', 'z_top','z_bottom','c_1','c_2','c_3','alfa_e'] 
    #Create plot figure
    fig = plt.figure()
    plt.subplot(131)
    plt.plot(np.cumsum(elastic[::-1])[::-1],-depths,color = 'r')
    plt.plot(np.cumsum((creep +elastic)[::-1])[::-1],-depths,color = 'orange')
    plt.plot(total[::-1],-depths,color = 'green')
    plt.subplot(132)
    plt.plot(total[::-1], -depths)
    plt.subplot(133)
    plt.plot(iz,-depths, color = 'r')    
   # Log output
    if verbose:
        log("delta_p:", delta_p)
        log("c_1:", c_1)
        log("c_2:", c_2)
        log("c_3:", c_3)
        log("zp:", zp)
        log("z_top:",z_top)
        log("z_bottom:", z_bottom)
        log("overburden / sigma_v1_eff:", overburden)
        log("delta_p:", delta_p)
        log("i_zp:", i_zp)
        log("iz", max(iz))
        log("settlement:", total[-1],total[0]) 
        log("result: ", result)
    return dict(zip(cols,args))

