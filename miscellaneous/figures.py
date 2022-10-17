import numpy as np
import matplotlib.pyplot as plt


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

