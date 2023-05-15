import numpy as np
import matplotlib.pyplot as plt
import matplotlib.path as mpath
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import shapely

COLORS_IC = ['#f19e45', '#b8a365', '#76c0a2', '#469186', '#4d567c', '#bb6639']

def make_settlement_plots(sps, lf, settlements, settlement_val_limit=0.025):

    sps[0].plot(np.cumsum(settlements['elastic'][::-1])[::-1], -lf.depth, lw=1.2, c='lightgreen', label = 'Elastic')
    sps[0].plot(np.cumsum((settlements['creep'] + settlements['elastic'])[::-1])[::-1], -lf.depth, lw=1.2, c='royalblue', label = 'Creep')
    sps[0].plot(np.cumsum(settlements['consolidation'][::-1])[::-1], -lf.depth, lw=1.2, c='salmon', label = 'Consolidation')
    sps[0].axhline(lf.gwl, c='cornflowerblue', ls="--", lw=1.5)

    sps[1].plot(settlements['settlement'][::-1], -lf.depth, lw=2, color='indigo')
    sps[1].text(0.95, 0.01, f"Max. Settlement = {round(max(settlements['settlement']),3)}m",
        verticalalignment='bottom', horizontalalignment='right',
        transform=sps[1].transAxes,
        )


    sps[1].axvline(settlement_val_limit, c='pink', ls = "--")
    #sps[2].plot(settlements['iz'], -lf.depth, lw=1, color='coral')


    sps[0].set_ylabel('Depth [m]')
    sps[0].set_xlabel('Settlements [m]')
    sps[0].legend()

    sps[1].set_xlabel('Total Settlement[m]')
    #sps[2].set_xlabel('Strain Influence Factor')




def make_cpt_plots(sps, cpt, c="gray", x_origin=True, y_origin=True):

    sps[0].plot(cpt.q_c, cpt.depth, lw=1, c=c)
    sps[1].plot(cpt.f_s, cpt.depth, lw=1, c=c)
    sps[2].plot(cpt.u_2, cpt.depth, lw=1, c=c)
    sps[2].axhline(cpt.gwl, c=c, ls="--", lw=0.7)

    # Prepare y-axis
    if y_origin:
        ylim = sps[0].get_ylim()
        sps[0].set_ylim([0, ylim[1]])

    # Prepare x-axis
    if x_origin:
        xlim = sps[0].get_xlim()
        sps[0].set_xlim([0, xlim[1]])
        xlim = sps[1].get_xlim()
        sps[1].set_xlim([0, xlim[1]])
        xlim = sps[2].get_xlim()
        sps[2].set_xlim([0, xlim[1]])

    sps[0].set_ylabel("Depth [m]")
    sps[0].set_xlabel("q_c [kPa]")
    sps[1].set_xlabel("f_s [kPa]")
    sps[2].set_xlabel("u_2 [kPa]")


def color_filter(ics):
     colors =np.empty(len(ics), dtype='U30')
    #given the indexes, color_filter the ics based on colors
    #where ics is less than 1.31 -> red
     colors[ics<1.31] = COLORS_IC[0]
     colors[(1.31<=ics) & (ics<2.05)] = COLORS_IC[1]
     colors[(2.05<=ics) & (ics<2.6)] = COLORS_IC[2]
     colors[(2.6<=ics) & (ics<2.95)] = COLORS_IC[3]
     colors[(2.95<=ics) & (ics<3.6)] = COLORS_IC[4]
     colors[ics>=3.6] = COLORS_IC[5]


     return colors


def create_path_obj_from_tuple(path_data, ax, color = 'red'):
    codes,verts = zip(*path_data)
    path = mpath.Path(verts, codes)
    patch = mpatches.PathPatch(path, facecolor=color, alpha=0.80)
    ax.add_patch(patch)
    x, y = zip(*path.vertices)
    return x,y


def generate_massarsch_points(obj):
    """
    Creates a region of 3 polygons that represent the Massarsch compaction zones
    Then we create an np.array of Points with (qc,fs) coordinates
    Then we check if the points are contained in the polygons
    If they are, we return the color of the polygon

    """
    compactable = [(0, 3), (1, 9.33), (1.0, 100), (0, 100), (0, 3)]
    marginally_compactable = [(0, 1),(0, 3),(1, 9.33),(1, 100),(1.5, 100),(1.5, 13),(0, 1)]
    not_compactable = [(0, 1), (3, 1), (3, 100), (1.5, 100), (1.5, 13), (0, 1)]

    compactable_p = shapely.Polygon(compactable)
    marginally_compactable_p = shapely.Polygon(marginally_compactable)
    not_compactable_p = shapely.Polygon(not_compactable)


    colors_pp = np.empty(len(obj.depth), dtype='U30')
    # colors_pp.fill(COLORS_IC[4])
    colors_pp.fill(COLORS_IC[4])

    friction_ratio = obj.cpt.f_s/obj.cpt.q_t * 100 #in percentages
    points = np.array([shapely.Point(x,y) for x,y in zip(friction_ratio, obj.cpt.q_c/10**3)])
    compactable_mask = shapely.contains(compactable_p, points)
    marginally_compactable_mask = shapely.contains(marginally_compactable_p, points)
    not_compactable_mask = shapely.contains(not_compactable_p, points)

    colors_pp[compactable_mask] = COLORS_IC[0]
    colors_pp[marginally_compactable_mask] = COLORS_IC[2]
    colors_pp[not_compactable_mask] = COLORS_IC[4]

    return colors_pp




def create_soil_index_plot(obj, save = False):
    # Create subplots
    fig, axs = plt.subplots(nrows=1, ncols=3, figsize=(18, 12))

    # Plot 1
    FONTSIZE = 14
    indexes = [0, 1.31, 2.05, 2.6, 2.95, 3.6, ]
    axs[0].plot(obj.i_c, -obj.depth, color='yellow', alpha=1, linewidth=4)
    axs[0].set_xlabel('I(SBT)')
    axs[0].set_ylabel('Depth (m)')
    axs[0].set_title('SBT Index', fontsize=FONTSIZE, fontweight='bold')
    axs[0].set_xticks(indexes)

    axs[0].axvspan(0., 1.31, alpha=1, color=COLORS_IC[0])
    axs[0].axvspan(1.31, 2.05, alpha=1, color=COLORS_IC[1])
    axs[0].axvspan(2.05, 2.60, alpha=1, color=COLORS_IC[2])
    axs[0].axvspan(2.60, 2.95, alpha=1, color=COLORS_IC[3])
    axs[0].axvspan(2.95, 3.60, alpha=1, color=COLORS_IC[4])
    axs[0].axvspan(3.60, 4.00, alpha=1, color=COLORS_IC[5])

    axs[0].set_ylim([-obj.depth.max(), 0])
    axs[0].set_xlim([0, 4])


    # Plot 2
    colors_pp = generate_massarsch_points(obj)
    axs[1].set_ylim([-obj.depth.max(), 0.05])
    # axs[1].set_xticks(indexes)
    axs[1].barh(-obj.depth, obj.q_t / 10**3, height=0.01, color=colors_pp, alpha=0.75)
    axs[1].legend()
    axs[1].set_xlabel('Tip Resistance (MPa)')
    axs[1].set_ylabel('Depth (m)')
    axs[1].set_title('Cone Resistance, qt', fontsize = FONTSIZE, fontweight='bold')
    axs[1].grid()
    axs[1].plot(obj.q_t / 10**3, -obj.depth, color='black', linewidth=1.5)

    #limit axs[1] plot to size

    Path = mpath.Path
    compactable_path_data = [(Path.MOVETO, (0, 3)),
                             (Path.LINETO, (1, 9.33)),
                             (Path.LINETO, (1, 100)),
                             (Path.LINETO, (0, 100)),
                             (Path.CLOSEPOLY, (0, 3))]
    marginally_compactable = [(Path.MOVETO, (0, 1)),
                              (Path.LINETO, (0, 3)),
                              (Path.LINETO, (1, 9.33)),
                              (Path.LINETO, (1, 100)),
                              (Path.LINETO, (1.5, 100)),
                              (Path.LINETO, (1.5, 13)),
                              (Path.CLOSEPOLY, (0, 1))]
    not_compactable = [(Path.MOVETO, (0, 1)),
                       (Path.LINETO, (3, 1)),
                       (Path.LINETO, (3, 100)),
                       (Path.LINETO, (1.5, 100)),
                       (Path.LINETO, (1.5, 13)),
                       (Path.CLOSEPOLY, (0, 1))]

    x, y = create_path_obj_from_tuple(compactable_path_data, axs[2], color = COLORS_IC[0])
    _, __ = create_path_obj_from_tuple(marginally_compactable, axs[2], color = COLORS_IC[2])
    _,__ = create_path_obj_from_tuple(not_compactable, axs[2], color = COLORS_IC[4])
    axs[2].semilogy()
    axs[2].set_xlim(0,3)
    axs[2].set_ylim(1,100)
    axs[2].set_xlabel('Friction Ratio %')
    axs[2].set_ylabel('Cone Penetration Resistance MPa')
    axs[2].legend(['Compactable', 'Marginally Compactable', 'Not Compactable'])
    axs[2].set_title('S.C. for Deep Compaction Works', fontsize = FONTSIZE, fontweight='bold')
    axs[2].scatter( obj.cpt.f_s/obj.q_t * 100, obj.cpt.q_c/10**3 , color = 'red', marker = 'o', s = 10)
    axs[2].plot(x,y, color = 'blue', linewidth = 2)
    if save:
        plt.savefig(obj.cpt.file_name + '.png', dpi=300)
    plt.show()











#
#
# bf, sps = plt.subplots(ncols=4, sharey=True, figsize=(8, 6))
# lq.fig.make_bi2014_outputs_plot(sps, bi2014)
#
# miscellaneous = plt.figure()
# # plt.subplot(131)
# # plt.plot(np.cumsum(elastic[::-1])[::-1], -lf.depth, color='r')
# # plt.plot(np.cumsum((creep + elastic)[::-1])[::-1], -lf.depth, color='orange')
# # plt.plot(settlement[::-1], -lf.depth, color='green')
# # plt.subplot(132)
# # plt.plot(settlement[::-1], -lf.depth)
# # plt.subplot(133)
# # plt.plot(iz, -lf.depth, color='r')
# # plt.show()



