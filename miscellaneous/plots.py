import numpy as np
import matplotlib
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
from matplotlib.lines import Line2D
from calc.liquefaction import run_rw1997, run_rw1997_gi, run_rw1997_fill
# from calc.fill_liquefaction import run_rw1997_fill
from miscellaneous.timed import timed
import matplotlib.pyplot as plt
GWL = 0.6

def pad_array(arr, max_size):
    return [np.pad(row, (0, max_size - row.size), 'constant', constant_values=(0, np.nan))
            for row in arr]


def calc_min(arr):
    return np.nanmin(arr, axis=0)


def calc_mean(arr):
    return np.nanmean(arr, axis=0)


def calc_max(arr):
    return np.nanmax(arr, axis=0)


def calc_max_depth(max_size):
    max_depth = np.arange(0.01, max_size / 100 + 0.01, 0.01)
    return max_depth


def generate_plot(sps, arr, max_size):
    padded = pad_array(arr, max_size)
    depth = calc_max_depth(max_size)

    mins = calc_min(padded)
    maxs = calc_max(padded)
    means = calc_mean(padded)
    # 3da4ab • #f6cd61 • #fe8a71
    sps.plot(mins, -depth, color='#fe8a71', lw=2.5)
    sps.plot(maxs, -depth, color='#3da4ab', lw=2.5)
    sps.plot(means, -depth, color='#f6cd61', lw=2.5, ls='--')


def label_x_ticks(sps, major_tick, minor_tick):
    sps.xaxis.set_major_locator(MultipleLocator(major_tick))
    sps.xaxis.set_minor_locator(MultipleLocator(minor_tick))
    sps.tick_params(axis='x', which='minor', length=10, direction='inout')

@timed
def create_cpt_9_plot(cpts):
    bf, ax = plt.subplots(3, 3, sharey=True, figsize=(8, 12))

    qcs = []
    phis = []
    fss = []
    u2s = []
    ems = []
    ics = []

    uws = []
    foss = []
    kks = []
    sus = []
    depths = []

    depths_26 = []
    sus_26 = []

    max_size = 0

    for i, cpt in enumerate(cpts):
        gwl = cpt.elevation[0] - GWL
        rw = run_rw1997(cpt, pga=0.122, m_w=6, gwl=gwl)

        if rw.cpt.q_c.size > max_size:
            max_size = rw.cpt.q_c.size

        qcs.append(rw.cpt.q_c / 10 ** 3)  # MPa
        fss.append(rw.cpt.f_s)
        u2s.append(rw.cpt.u_2)

        ems.append(rw.elastic_modulus / 10 ** 3)  # MPa
        ics.append(rw.i_c)
        phis.append(rw.phi)
        depths.append(rw.depth)

        uws.append(rw.unit_wt)
        foss.append(rw.factor_of_safety)
        kks.append(rw.permeability)
        sus.append(rw.s_u)

        depths_26.append(rw.depth[rw.i_c > 2.6])
        sus_26.append(rw.s_u[rw.i_c > 2.6])

        ax[0, 0].plot(rw.cpt.q_c / 10 ** 3, -rw.depth, color='gray', alpha=.3)
        ax[0, 1].plot(rw.cpt.f_s, -rw.depth, color='gray', alpha=.3)
        ax[0, 2].plot(rw.i_c, -rw.depth, color='gray', alpha=.3)

        ax[1, 0].plot(rw.elastic_modulus / 10 ** 3, -rw.depth, color='gray', alpha=.3)
        ax[1, 1].plot(rw.phi, -rw.depth, color='gray', alpha=.3)
        ax[1, 2].plot(rw.unit_wt, -rw.depth, color='gray', alpha=.3)

        ax[2, 0].plot(rw.factor_of_safety, -rw.depth, color='gray', alpha=.3)
        ax[2, 1].scatter(rw.s_u[rw.i_c > 2.6], - rw.depth[rw.i_c > 2.6], color='gray', alpha=.3)
        ax[2, 2].plot(rw.permeability, -rw.depth, color='gray', alpha=.3)

        ax[0, 0].grid(True, alpha=0.5)
        ax[0, 0].set_xlim(0, 30)
        ax[0, 0].set_xlabel('Cone resistance qc (MPa)')
        ax[0, 0].set_ylabel('Depth (m)')
        label_x_ticks(ax[0, 0], 5, 1)

        # ax[0,0].set_xticks(np.round(range(2,30,2)),minor = True)
        ax[0, 0].tick_params(axis='y')

        ax[0, 1].grid(True, alpha=0.5)
        ax[0, 1].set_xlabel('Skin friction resistance f_s kPa')
        customlines = [Line2D([0], [0], color='#fe8a71', lw=4),
                       Line2D([0], [0], color='#3da4ab', lw=4),
                       Line2D([0], [0], color='#f6cd61', lw=4),
                       Line2D([0], [0], color='gray', lw=4)]
        ax[0, 1].legend(customlines, ['Minimum', 'Maximum', 'Mean', 'CPTs'], loc='lower right')

        ax[0, 2].grid(True, alpha=0.5)
        ax[0, 2].set_xlim([0, 3])
        ax[0, 2].set_xlabel('SBT type index')
        IC_LIMITS = [0, 1.3, 1.8, 2.1, 2.6, 4]
        ax[0, 2].set_xticks(IC_LIMITS)

        ax[1, 0].grid(True, alpha=0.5)
        ax[1, 0].set_xlim(0, 55)
        ax[1, 0].set_xlabel('Elastic Modulus (MPa)')
        ax[1, 0].set_ylabel('Depth (m)')
        label_x_ticks(ax[1, 0], 10, 2.5)

        ax[1, 1].grid(True, alpha=0.5)
        ax[1, 1].set_xlim(27, 45)
        ax[1, 1].set_xlabel('Friction Angle (degrees)')
        label_x_ticks(ax[1, 1], 5, 1)

        ax[1, 2].grid(True, alpha=0.5)
        ax[1, 2].set_xlabel('Unit Weights (kN/m3)')
        label_x_ticks(ax[1, 2], 2, 0.5)

        ax[2, 0].grid(True, alpha=0.5)
        ax[2, 0].set_xlabel('FoS - Liquefaction')
        ax[2, 0].axvline(x=1.25, c='black', ls='--', lw=2.5)
        ax[2, 0].set_xlim(0.5, 2.25)
        ax[2, 0].set_ylabel('Depth (m)')

        ax[2, 1].grid(True, alpha=0.5)
        ax[2, 1].set_xlabel('Undrained SHear Strength su (kPa)')
        ax[2, 1].set_xlim(0, 100)
        label_x_ticks(ax[2, 1], 25, 5)
        ax[2, 1].legend([Line2D([0], [0], marker='o', color='w', label='Scatter',
                                markerfacecolor='gray', alpha=0.5, markersize=15)], ['su where i_c > 2.6'])
        #     ax[2,1].xaxis.set_major_locator(MultipleLocator(50))
        #     ax[2,1].xaxis.set_minor_locator(MultipleLocator(10))
        #     ax[2,1].tick_params(axis = 'x', which ='minor', length = 10, direction = 'inout')

        ax[2, 2].grid(True)
        ax[2, 2].set_xlabel('Permeability m/s')
        # ax[2,2].set_xlim(0.0000000001, 0.000001)
        ax[2, 2].set_xscale('log')
        ax[2, 2].set_xticks([10 ** i for i in range(-9, 1, 2)])

    depth = calc_max_depth(max_size)

    generate_plot(ax[0, 0], qcs, max_size)
    generate_plot(ax[0, 1], fss, max_size)
    generate_plot(ax[0, 2], ics, max_size)
    generate_plot(ax[1, 0], ems, max_size)
    generate_plot(ax[1, 1], phis, max_size)
    generate_plot(ax[1, 2], uws, max_size)

    generate_plot(ax[2, 0], foss, max_size)
    generate_plot(ax[2,1],sus_26,max_size)
    # generate_plot(ax[2, 2], kks, max_size)

    matplotlib.rcParams.update({'font.size': 14})
    plt.show()
    bf.savefig('cpt_grid_chart_plot.pdf', papertype='a4', bbox_inches='tight')






def create_cpt_9_colored(cpts):
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D

    # Define the colors for each CPT
    cpt_colors = ['red', 'blue', 'green', 'orange', 'purple', 'cyan', 'magenta', 'yellow', 'black']

    bf, ax = plt.subplots(3, 3, sharey=True, figsize=(20, 40))

    qcs = []
    phis = []
    fss = []
    u2s = []
    ems = []
    ics = []

    uws = []
    foss = []
    kks = []
    sus = []
    depths = []

    depths_26 = []
    sus_26 = []

    max_size = 0

    for i, x in enumerate(dfs['Object']):
        rw = run_rw1997(x, pga=0.122, m_w=6, gwl=round(float(dfs['groundlvl'][i]) - GWL, 2))  # GL - 0.5m WL

        if rw.cpt.q_c.size > max_size:
            max_size = rw.cpt.q_c.size

        qcs.append(rw.cpt.q_c / 10 ** 3)  # MPa
        fss.append(rw.cpt.f_s)
        u2s.append(rw.cpt.u_2)
        ems.append(rw.elastic_modulus / 10 ** 3)  # MPa
        ics.append(rw.i_c)
        phis.append(rw.phi)
        depths.append(rw.depth)

        rw.depth = rw.depth - float(max(dfs['groundlvl']))

        uws.append(rw.unit_wt)
        foss.append(rw.factor_of_safety)
        kks.append(rw.permeability)
        sus.append(rw.s_u)

        depths_26.append(rw.depth[rw.i_c > 2.6])
        sus_26.append(rw.s_u[rw.i_c > 2.6])

        ax[0, 0].plot(rw.cpt.q_c / 10 ** 3, -rw.depth, color=cpt_colors[i % len(cpt_colors)], alpha=0.5)
        ax[0, 1].plot(rw.cpt.f_s, -rw.depth, color=cpt_colors[i % len(cpt_colors)], alpha=0.5)
        ax[0, 2].plot(rw.i_c, -rw.depth, color=cpt_colors[i % len(cpt_colors)], alpha=0.5)
        ax[1, 0].plot(rw.elastic_modulus / 10 ** 3, -rw.depth, color=cpt_colors[i % len(cpt_colors)], alpha=0.5)
        ax[1, 1].plot(rw.phi, -rw.depth, color=cpt_colors[i % len(cpt_colors)], alpha=0.5)
        ax[1, 2].plot(rw.unit_wt, -rw.depth, color=cpt_colors[i % len(cpt_colors)], alpha=0.5)
        ax[2, 0].plot(rw.factor_of_safety, -rw.depth, color=cpt_colors[i % len(cpt_colors)], alpha=0.5)
        ax[2, 2].plot(rw.permeability, -rw.depth, color=cpt_colors[i % len(cpt_colors)], alpha=0.5)

    # Remove min, max, and mean labels
    ax[0, 1].legend([], [], frameon=False)
    ax[0, 1].set_title('')

    # Create a custom legend with CPT colors
    custom_lines = [Line2D([0], [0], color=color, lw=2) for color in cpt_colors]
    ax[0, 1].legend(custom_lines, [f'CPT {i + 1}' for i in range(len(dfs['Object']))], loc='lower right')

    # Set grid and axis labels for each subplot
    ax[0, 0].grid(True, alpha=0.5)
    ax[0, 0].set_xlim(0, 30)
    ax[0, 0].set_xlabel('Cone resistance qc (MPa)')
    ax[0, 0].set_ylabel('Elevation (m NADD)')

    ax[0, 1].grid(True, alpha=0.5)
    ax[0, 1].set_xlabel('Skin friction resistance fs (kPa)')

    ax[0, 2].grid(True, alpha=0.5)
    ax[0, 2].set_xlim([0, 3])
    ax[0, 2].set_xlabel('SBT type index')
    IC_LIMITS = [0, 1.3, 1.8, 2.1, 2.6, 4]
    ax[0, 2].set_xticks(IC_LIMITS)

    ax[1, 0].grid(True, alpha=0.5)
    ax[1, 0].set_xlim(0, 55)
    ax[1, 0].set_xlabel('Elastic Modulus (MPa)')
    ax[1, 0].set_ylabel('Elevation (m NADD)')

    ax[1, 1].grid(True, alpha=0.5)
    ax[1, 1].set_xlim(27, 45)
    ax[1, 1].set_xlabel('Friction Angle (degrees)')

    ax[1, 2].grid(True, alpha=0.5)
    ax[1, 2].set_xlabel('Unit Weights (kN/m3)')

    ax[2, 0].grid(True, alpha=0.5)
    ax[2, 0].set_xlabel('FoS - Liquefaction')
    ax[2, 0].axvline(x=1.25, c='black', ls='--', lw=2.5)
    ax[2, 0].set_xlim(0.5, 2.25)
    ax[2, 0].set_ylabel('Elevation (m NADD)')

    ax[2, 1].grid(True, alpha=0.5)
    ax[2, 1].set_xlabel('Undrained Shear Strength su (kPa)')
    ax[2, 1].set_xlim(0, 100)

    ax[2, 2].grid(True)
    ax[2, 2].set_xlabel('Permeability m/s')
    ax[2, 2].set_xscale('log')
    ax[2, 2].set_xticks([10 ** i for i in range(-9, 1, 2)])

    depth = calc_max_depth(max_size)

    generate_plot(ax[0, 0], qcs, max_size)
    generate_plot(ax[0, 1], fss, max_size)
    generate_plot(ax[0, 2], ics, max_size)
    generate_plot(ax[1, 0], ems, max_size)
    generate_plot(ax[1, 1], phis, max_size)
    generate_plot(ax[1, 2], uws, max_size)

    generate_plot(ax[2, 0], foss, max_size)
    generate_plot(ax[2, 2], kks, max_size)

    matplotlib.rcParams.update({'font.size': 14})

    bf.savefig(folder_path + 'pre_charts.pdf', papertype='a3', bbox_inches='tight')

    pass



@timed
def create_cpt_before_and_after(cpts):
    bf, ax = plt.subplots(1, 2, sharey=True, figsize=(12, 36))
    #print(ax)
    foss_rw = []
    foss_fill = []


    depths = []

    max_size = 0

    for i, cpt in enumerate(cpts):
        rw = run_rw1997(cpt, pga=0.122, m_w=6, gwl=2)
        rw_fill = run_rw1997_fill(cpt, pga=0.122, m_w=6, gwl=2, fill_gamma=17, fill_height=8)

        if rw.cpt.q_c.size > max_size:
            max_size = rw.cpt.q_c.size

        depths.append(rw.depth)

        foss_rw.append(rw.factor_of_safety)
        foss_fill.append(rw_fill.factor_of_safety)

        ax[0].plot(rw.factor_of_safety, -rw.depth, color='gray', alpha=.3)
        ax[1].plot(rw_fill.factor_of_safety, -rw.depth, color='gray', alpha=.3)


        ax[0].grid(True, alpha=0.5)
        ax[0].set_xlabel('FoS - Liquefaction - Before improvement')
        ax[0].axvline(x=1.25, c='black', ls='--', lw=2.5)
        ax[0].set_xlim(0.5, 2.25)
        ax[0].set_ylabel('Depth (m)')
        customlines = [Line2D([0], [0], color='#fe8a71', lw=4),
                       Line2D([0], [0], color='#3da4ab', lw=4),
                       Line2D([0], [0], color='#f6cd61', lw=4),
                       Line2D([0], [0], color='gray', lw=4)]
        ax[0].legend(customlines, ['Minimum', 'Maximum', 'Mean', 'CPTs'], loc='lower left')

        ax[1].grid(True, alpha=0.5)
        ax[1].set_xlabel('FoS - Liquefaction - After improvement')
        ax[1].axvline(x=1.25, c='black', ls='--', lw=2.5)
        ax[1].set_xlim(0.5, 2.25)
        ax[1].set_ylabel('Depth (m)')
        ax[1].legend(customlines, ['Minimum', 'Maximum', 'Mean', 'CPTs'], loc='lower left')


    depth = calc_max_depth(max_size)

    generate_plot(ax[0], foss_rw, max_size)
    generate_plot(ax[1], foss_fill, max_size)

    matplotlib.rcParams.update({'font.size': 14})
    plt.show()
    bf.savefig('cpt_2_chart_plot.png', papertype='a3', bbox_inches='tight')



@timed
def create_plots_liq_gi_fill(cpts,gi,fill_gamma,fill_height):
    bf, ax = plt.subplots(1, 3, sharey=True, figsize=(12, 36))
    #print(ax)
    foss_rw = []
    foss_rw_fill = []
    foss_rw_gi = []

    depths = []

    max_size = 0

    for i, cpt in enumerate(cpts):
        rw = run_rw1997(cpt, pga=0.122, m_w=6, gwl=2)
        rw_fill = run_rw1997_fill(cpt, pga=0.122, m_w=6, gwl=2, fill_gamma=17, fill_height=8)
        rw_gi = run_rw1997_gi(rw,gi)
        if rw.cpt.q_c.size > max_size:
            max_size = rw.cpt.q_c.size

        depths.append(rw.depth)

        foss_rw.append(rw.factor_of_safety)
        foss_rw_fill.append(rw_fill.factor_of_safety)
        foss_rw_gi.append(rw_gi.factor_of_safety)

        ax[0].plot(rw.factor_of_safety, -rw.depth, color='gray', alpha=.3)
        ax[1].plot(rw_fill.factor_of_safety, -rw.depth, color='gray', alpha=.3)
        ax[2].plot(rw_gi.factor_of_safety, -rw.depth, color='gray', alpha=.3)


        ax[0].grid(True, alpha=0.5)
        ax[0].set_xlabel('FoS - Liquefaction - RW1997')
        ax[0].axvline(x=1.25, c='black', ls='--', lw=2.5)
        ax[0].set_xlim(0.5, 2.25)
        ax[0].set_ylabel('Depth (m)')
        customlines = [Line2D([0], [0], color='#fe8a71', lw=4),
                       Line2D([0], [0], color='#3da4ab', lw=4),
                       Line2D([0], [0], color='#f6cd61', lw=4),
                       Line2D([0], [0], color='gray', lw=4)]
        ax[0].legend(customlines, ['Minimum', 'Maximum', 'Mean', 'CPTs'], loc='lower left')

        ax[1].grid(True, alpha=0.5)
        ax[1].set_xlabel('FoS - Liquefaction - RWFILL')
        ax[1].axvline(x=1.25, c='black', ls='--', lw=2.5)
        ax[1].set_xlim(0.5, 2.25)
        ax[1].set_ylabel('Depth (m)')
        ax[1].legend(customlines, ['Minimum', 'Maximum', 'Mean', 'CPTs'], loc='lower left')

        ax[2].grid(True, alpha=0.5)
        ax[2].set_xlabel('FoS - Liquefaction - RWGI')
        ax[2].axvline(x=1.25, c='black', ls='--', lw=2.5)
        ax[2].set_xlim(0.5, 2.25)
        ax[2].set_ylabel('Depth (m)')
        ax[2].legend(customlines, ['Minimum', 'Maximum', 'Mean', 'CPTs'], loc='lower left')

    depth = calc_max_depth(max_size)

    generate_plot(ax[0], foss_rw, max_size)
    generate_plot(ax[1], foss_rw_fill, max_size)
    generate_plot(ax[2], foss_rw_gi, max_size)

    matplotlib.rcParams.update({'font.size': 14})
    plt.show()
    bf.savefig('cpt_3_chart_plot.png', papertype='a3', bbox_inches='tight')



# import glob
# import glob
# paths = glob.glob('D:/01_Projects/38.Al Hudayriyat/post data/processed/' + '*.csv')
#
# gpath = ''
# scf = 1.3
# from load.loading import load_mpa_cpt_file
# cpts = [load_mpa_cpt_file(path, scf = scf) for path in paths]
#
# create_cpt_9_plot(cpts)