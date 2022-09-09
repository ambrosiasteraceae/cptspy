import os
import liquepy as lq
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from scipy import integrate


plt.rcParams.update({'figure.max_open_warning': 0})
# cpt = lq.field.load_mpa_cpt_file("CPT_H15c.csv", delimiter=";")
# bi2014 = lq.trigger.run_bi2014(cpt, m_w=7.5, pga=0.25, gwl=0)
#

def load_cpt(cptfile):
    data = pd.read_excel(cptfile)

    data1 = data['Depth [m]']
    data2 = data['Cone resistance (qc) in MPa']
    data3 = data['Soil Classification (using Bq)']

    depth =np.around(np.array(data1),2)
    q_c =np.array(data2)
    soil_type =np.array(data3)

    return depth,q_c,soil_type



def corrected_q_c(q_c,depth):
    q_c = np.where(q_c<15,q_c,15)
    for i,x in enumerate(depth):
        if x < 8:
            q_c[i]*=-1
    return q_c


def corrected_q_c_rev2(cpt,downdrag):
    """
    Returns corrected q_c & downdrag if any
    """
    q_c = np.where(cpt.q_c < 15, cpt.q_c, 15)
    q_c_downdrag = np.where(cpt.depth < 8, cpt.q_c * -1, )

def pile_class_shaft_factor(soil_type, q_c, pile_class):
    n = len(soil_type)
    alfa_s = np.ones(n)
    for i in range(n):
        b = soil_type[i]
        ##### Soil Number 0 to 4 including ####
        if soil_type[i] <= 4 and q_c[i] < 3:
            alfa_s[i] = 0.020
        if soil_type[i] <= 4 and q_c[i] > 3:
            alfa_s[i] = 0.030
        ##### Soil Number 5 ####
        if soil_type[i] == 5:
            alfa_s[i] = 0.025
        ##### Soil Number 6 ####
        if soil_type[i] == 6 and pile_class == 'driven':
            alfa_s[i] = 0.012
        if soil_type[i] == 6 and pile_class == 'bored/cfa':
            alfa_s[i] = 0.006
        ##### Soil Number 7 ####
        if soil_type[i] == 7 and pile_class == 'driven':
            alfa_s[i] = 0.012 * 0.75
        if soil_type[i] == 7 and pile_class == 'bored/cfa':
            alfa_s[i] = 0.006 * 0.75
        #### Soil number 8 and 9 ####
        if soil_type[i] >= 8 and pile_class == 'driven':
            alfa_s[i] = 0.012
        if soil_type[i] >= 8 and pile_class == 'bored/cfa':
            alfa_s[i] = 0.006

    return alfa_s

def pile_class_shaft_factor_rev2():
    cond_1 = np.where(lf.i_c<=1.3)
    cond_2 = np.where((lf.i_c>1.3) & (lf.i_c<=1.8))
    cond_3 = np.where((lf.i_c>1.8) & (lf.i_c<=2.1))
    cond_4 = np.where((lf.i_c>2.1) & (lf.i_c<2.6))
    cond_5 = np.where(lf.i_c>=2.6)
    lf.i_c[cond_1] = 0.02
    lf.i_c[cond_2] = 0.04
    lf.i_c[cond_3] = 0.06
    lf.i_c[cond_4] = 0.08
    lf.i_c[cond_5] = 0.10

    IC_LIMITS = [0, 1.3, 1.8, 2.1, 2.6, 4]
    lim1 = [0, 1.3]
    pass

def pile_class_tip_factor(pile_class):
    if pile_class == 'driven':
        alfa_b = 0.5
    if pile_class =='bored/cfa':
        alfa_b = 0.5
    return alfa_b

def method_safety_factors(pile_class):
    if pile_class =='driven':
        gamma_b = 1.1
        gamma_s = 1.1
    if pile_class == 'bored/cfa':
        gamma_b = 2
        gamma_s = 1.5
    return gamma_b, gamma_s

def safety_factors_design_approach_r1(pile_class):
    if pile_class == 'driven':
        sf_tip = 1
        sf_shaft = 1
    if pile_class == 'bored/cfa':
        # Do check SF TIP AND SF Shaft in case of either bored or CFA currently bored/cfa is for bored
        sf_tip = 1.25
        sf_shaft = 1.0
    return sf_tip, sf_shaft

def safety_factors_design_approach_r4(pile_class):
    if pile_class == 'driven':
        sf_tip = 1.3
        sf_shaft = 1.3
    if pile_class == 'bored/cfa':
        # Do check SF TIP AND SF Shaft in case of either bored or CFA currently bored/cfa is for bored
        sf_tip = 1.6
        sf_shaft = 1.3
    return sf_tip, sf_shaft

def numberofcpt_safety_factors(number_of_soundings):
    if number_of_soundings == 1:
        safety_factor=1.6
    elif number_of_soundings == 2:
        safety_factor=1.45
    elif number_of_soundings == 3:
        safety_factor=1.35
    elif number_of_soundings == 4:
        safety_factor = 1.27
    elif number_of_soundings == 5:
        safety_factor = 1.21
    elif number_of_soundings>5 and number_of_soundings<=7:
        safety_factor = 1.21
    elif number_of_soundings>7 and number_of_soundings <10:
        safety_factor = 1.16
    elif number_of_soundings >=10:
        safety_factor = 1.10
    return safety_factor




def maximum_shaft_resistance(alfa_s,q_c_cor):
    #We will not take the maximum negative force it will develop. A 0.5 factor is applied.
    q_c_shaft = np.where(q_c_cor<0,q_c_cor*0.5,q_c_cor)
    return q_c_shaft * alfa_s

def findindex(index_to_find,depth):
    for i in range (len(depth)):
        if index_to_find == depth[i]:
            return i

def average_qc(index_to_find,qc,depth):
     s = 0
     t = 0
     if index_to_find < 0.60:
         return qc[findindex(index_to_find,depth)]
     for i in range(findindex(index_to_find,depth)-60,findindex(index_to_find,depth)+240):
         s += qc[i]
         t += 1
     return s/t

def all_avg(qc,depth):
    a = []
    for i in range(len(depth)-240):
        q = average_qc(depth[i],qc,depth)
        a.append(q)
    return np.asarray(a)


def write_to_txt(bearing_capacity_r1,depth,cptfile):
    outfile = open("rezultate+{}.txt".format(cptfile), "w")
    for j in range(len(bearing_capacity_r1)):
        outfile.write("depth is {} and qc is {}\n".format(depth[j], bearing_capacity_r1[j]))
    outfile.close()


def plot_q_c(depth, q_c, q_c_cor, q_c_average, length, diameter, save, show, cptfile, pr_max_base):
    # Position at end of pile length
    bf = plt.figure(figsize=(10, 14), dpi=150)
    colors = ['limegreen', 'darkorange', 'mediumslateblue', 'dodgerblue']
    labels = ['Measured Qc', 'Corrected Qc', 'Averaged Qc', 'Prmax base']
    graphs = [q_c, q_c_cor, q_c_average]
    plt.plot(np.abs(q_c), -depth, lw=3, color=colors[0], label=labels[0])
    plt.plot(np.abs(q_c_cor), -depth, lw=3, color=colors[1], label=labels[1])
    plt.plot(q_c_average, -depth[:len(q_c_average)], lw=3, color=colors[2], label=labels[2])
    plt.plot(pr_max_base, -depth[:len(q_c_average)], lw=3, color=colors[3], label=labels[3])
    plt.grid(color='0.75', ls='--', lw=1)
    plt.xlabel("Maximum Qc (MPa)")
    plt.ylabel("Depth (m)")
    plt.legend(loc='upper right')
    filepath = os.path.dirname(__file__) + "/ForDarius/"
    name = "{}Tip resistances for D={} and Length = {}mm".format(cptfile[:14], diameter, int(length * 1000))
    if save:
        figure_ffp = filepath + name
        plt.savefig(figure_ffp, dpi=150)
    if show:
        plt.show()


def plot_step_q_s(depth, q_s,length,diameter,save,show,cptfile,x):
    bf = plt.figure(figsize=(10, 14), dpi=150)
    negative_index = findindex(8,depth)
    colors = 'orchid'
    labels = 'Qs kN'
    q_shafty = q_s[:x] * np.pi * diameter
    depth_y = -depth[:x]

    plt.plot(q_shafty, depth_y, lw=3, label=labels, color=colors, alpha=0.9)

    plt.fill_betweenx(depth_y[:negative_index], q_shafty[:negative_index], facecolor='red', alpha=0.2)
    plt.fill_betweenx(depth_y[negative_index:x], q_shafty[negative_index:x], facecolor='green', alpha=0.2)
    plt.grid(color='0.75', ls='--', lw=1)
    plt.xlabel("Rs (kN)")
    plt.ylabel("Depth (m)")
    plt.legend(loc='upper right')
    filepath = os.path.dirname(__file__) + "/ForDarius/"
    name = "{}Shaft Friction for D={} and Length = {}mm".format(cptfile[:14],diameter,int(length*1000))
    if save:
        figure_ffp = filepath + name
        plt.savefig(figure_ffp, dpi=150)
    if show:
        plt.show()


def plot_design_approach_R1(depth,shaft_force_r1,tip_force_r1,bearing_capacity_r1,length,diameter,save,show,cptfile,x):

    bf = plt.figure(figsize=(10,14),dpi=150)
    linestyles =['o','o','o']
    colors =['limegreen','darkorange','dodgerblue']
    labels =['Shaft Resistance R1','Tip Resistance R1','Bearing Capacity for Compression R1']
    graphs = [shaft_force_r1,tip_force_r1,bearing_capacity_r1]
    for i, graph in enumerate(graphs):
        plt.plot(graph[:x],-depth[:x],lw=3,label=labels[i],color=colors[i])

    max_bear_force = bearing_capacity_r1[:x]
    maxim = np.asscalar(max_bear_force[-1])


    #plt.ylim(0,len(depth))
    plt.grid(color='0.75',ls='--',lw=1)
    plt.xlabel("Maximum bearing force (kN)")
    plt.ylabel("Depth (m)")
    plt.legend(loc='upper right')
    plt.text(maxim-maxim*0.2, -depth[x]+0.5, r'$Rcd = %i kN $'
             % maxim, {'color': 'black', 'fontsize': 12})
    filepath = os.path.dirname(__file__) + "/ForDarius/"
    name = "{}BearingCapacityR1 for D={}mm and Length = {}mm".format(cptfile[:14],diameter,int(length*1000))
    if save:
        figure_ffp = filepath + name
        plt.savefig(figure_ffp, dpi=150)
    if show:
        plt.show()

def plot_design_approach_R4(depth,shaft_force_r4,tip_force_r4,bearing_capacity_r4,length,diameter,save,show,cptfile,x):

    bf = plt.figure(figsize=(10,14),dpi=150)
    linestyles =['o','o','o']
    colors =['limegreen','darkorange','dodgerblue']
    labels =['Shaft Resistance R4','Tip Resistance R4','Bearing Capacity for Compression R4']
    graphs = [shaft_force_r4,tip_force_r4,bearing_capacity_r4]
    for i, graph in enumerate(graphs):
        plt.plot(graph[:x],-depth[:x],lw=3,label=labels[i],color=colors[i])

    max_bear_force = bearing_capacity_r4[:x]
    maxim = np.asscalar(max_bear_force[-1])


    #plt.ylim(0,len(depth))
    plt.grid(color='0.75',ls='--',lw=1)
    plt.xlabel("Maximum bearing force (kN)")
    plt.ylabel("Depth (m)")
    plt.legend(loc='upper right')
    plt.text(maxim-maxim*0.2, -depth[x]+0.5, r'$Rcd = %i kN $'
             % maxim, {'color': 'black', 'fontsize': 12})
    filepath = os.path.dirname(__file__) + "/ForDarius/"
    name = "{}BearingCapacityR4 for D={}mm and Length = {}mm".format(cptfile[:14],diameter,int(length*1000))
    if save:
        figure_ffp = filepath + name
        plt.savefig(figure_ffp, dpi=150)
    if show:
        plt.show()



def calculate(diameter,pile_class,number_of_soundings,length,cptfile,show,save):

    depth,q_c,soil_type = load_cpt(cptfile)
    x = findindex(length, depth)  # Position at end of pile length
    area = (np.pi * (diameter)**2)/4
    circumference = np.pi * diameter

    q_c_cor = corrected_q_c(q_c, depth)
    q_c_average = all_avg(abs(q_c_cor), depth)

    alfa_s = pile_class_shaft_factor(soil_type, q_c, pile_class)
    alfa_b = pile_class_tip_factor(pile_class)

    gamma_b, gamma_s = method_safety_factors(pile_class)
    epsilon_safety_factor = numberofcpt_safety_factors(number_of_soundings)
    sf_tip_r1, sf_shaft_r1 = safety_factors_design_approach_r1(pile_class)
    sf_tip_r4, sf_shaft_r4 = safety_factors_design_approach_r4(pile_class)


    pr_base_max = q_c_average * alfa_b
    tip_force = pr_base_max * area / 10**3
    tip_force_calculated = tip_force / gamma_b
    tip_force_car = tip_force / epsilon_safety_factor
    tip_force_r1 = tip_force_car / sf_tip_r1
    tip_force_r4 = tip_force_car / sf_tip_r4


    q_s = maximum_shaft_resistance(alfa_s,q_c_cor)
    q_s_integrated = integrate.cumtrapz(q_s,depth,initial=0)
    q_s_max = q_s_integrated
    shaft_force = q_s_max * circumference
    shaft_force_calculated = shaft_force / gamma_s
    shaft_force_car = shaft_force_calculated / epsilon_safety_factor
    shaft_force_r1 = shaft_force_car / sf_shaft_r1
    shaft_force_r4 = shaft_force_car / sf_shaft_r4

    bearing_capacity_r1 = tip_force_r1[:x] + shaft_force_r1[:x]
    bearing_capacity_r4 = tip_force_r4[:x] + shaft_force_r4[:x]


    #write_to_txt(bearing_capacity_r1, depth,cptfile)

    plot_q_c(depth, q_c, q_c_cor, q_c_average, length, diameter, save, show, cptfile, pr_base_max)
    plot_step_q_s(depth, q_s, length, diameter, save, show, cptfile,x)
    plot_design_approach_R1(depth, shaft_force_r1, tip_force_r1, bearing_capacity_r1,
                            length, diameter, save, show, cptfile,x)
    plot_design_approach_R4(depth, shaft_force_r4, tip_force_r4, bearing_capacity_r4,
                            length, diameter, save, show, cptfile, x)






calculate(600,'driven',10,25,save=1,show=1,cptfile = '2020-5_cpt 101.000.xls')
