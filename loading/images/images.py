import matplotlib.pyplot as plt
import numpy as np


FS_LOW_to_0p75 = (0.75, 0, 0)
FS_0p75_to_1p0 = (0.95, 0, 0)
FS_1p0_to_1p25 = (0.9, 0.4, 0.15)
FS_1p25_to_1p5 = (1, 0.65, 0.25)
FS_1p5_to_HIGH = (0.1, 0.6, 0.1)
FS_NON_LIQ = (0.4, 0.4, 0.4)
COLORS_IC = ['#f19e45', '#b8a365', '#76c0a2', '#469186', '#4d567c', '#bb6639']

COLORS_FOS = [FS_LOW_to_0p75, FS_0p75_to_1p0, FS_1p0_to_1p25, FS_1p25_to_1p5, FS_1p5_to_HIGH, FS_NON_LIQ]
layers = ['Gravelly Sand to Dense Sand', 'Clean Sand to Silty Sand', 'Silty Sand to Sandy Silt',
          'Clayey Silt to Silty Clay', 'Silty Clay to Clay', 'Organic Soils - Clay']
foses = ['FS < 0.75', '0.75 < FS < 1.0', '1.0 < FS < 1.25', '1.25 < FS < 1.5', 'FS > 1.5', 'Non-Liquefiable']

FONTSIZE = 12
TXTCOLOR = 'gray'
TXTWEIGHT = 'bold'
FIGURESIZE = (4, 4)
def generate_ic_legend():
    fig, ax = plt.subplots(1, 1, figsize=FIGURESIZE)
    plt.barh([1,2,3,4,5,6], [1,1,1,1,1,1], color=COLORS_IC[::-1], height = 1, edgecolor='black')
    ax.set_xlim(0, 4)
    ax.set_ylim(0.5, 7)
    for i, layer in enumerate(layers[::-1]):
        ax.text(1.1, i+0.8, layer, fontsize=FONTSIZE, color=TXTCOLOR, fontweight=TXTWEIGHT)
    ax.text(0.5, 7, 'Soil Index Legend', fontsize=FONTSIZE, color=TXTCOLOR, fontweight=TXTWEIGHT)
    ax.axis('off')
    fig.savefig('ic_legend.png', bbox_inches='tight')
    plt.show()


def generate_fos_legend():

    fig,ax = plt.subplots(1,1,figsize=FIGURESIZE)
    ax.barh([1,2,3,4,5,6], [1,1,1,1,1,1], color=COLORS_FOS[::-1], height = 1, edgecolor='black', alpha = 0.5)
    # ax.xlim(-1,4)
    # ax.ylim(-1,8)
    ax.set_xlim(0,4)
    ax.set_ylim(0.5,7)
    for i, fos in enumerate(foses[::-1]):
        ax.text(1.1, i+0.8, fos, fontsize=FONTSIZE, color=TXTCOLOR, fontweight=TXTWEIGHT)
    ax.text(0.5, 7, 'Factor of Safety Legend', fontsize=FONTSIZE, color=TXTCOLOR, fontweight=TXTWEIGHT)
    ax.axis('off')
    fig.savefig('fos_legend.png', bbox_inches='tight')
    plt.show()

generate_ic_legend()
generate_fos_legend()