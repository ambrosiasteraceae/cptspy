from loading.loading import load_dataframe
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
import pyqtgraph as pg
import random
import numpy as np
import shapely.geometry as shp
import glob
import json, os
#
# ffps = glob.glob('D:/04_R&D/cptspy/output/*.csv')
#
#
# path = 'D:/04_R&D/cptspy/output/'
#
# df = load_dataframe(ffps)
#
# df['Northing'] = df['Northing'].astype(float)
# df['Easting'] = df['Easting'].astype(float)
# northing = df['Northing'].values
# easting = df['Easting'].values
# ids = df['CPT-ID'].values
#
# colors = ['#ffe3b3', '#53d2dc', '#4f8fc0']
#
#
# color_array = np.random.choice(colors, ids.size)
#
#
# pg.setConfigOption('background', 'w')
#
# app = QApplication(sys.argv)
# win = QMainWindow()
# plt = pg.PlotWidget()
# plt.plot(easting, northing, pen=None, symbol='o', symbolSize=15, symbolBrush=color_array)
#
# plt.setAspectLocked(True)
#
# #Create a selection cursor to use with our plot
#
#
#
# win.setCentralWidget(plt)
# win.show()
#
# sys.exit(app.exec())

# ord()

a = {k:ord(k) for k in 'abcdfedgh'}
print(a)

ffp = os.getcwd()
name = '/project/project_settings/'
path = ffp+name
if not os.path.exists(path):
    os.makedirs(path)
with open(path+'requirements.json', 'w') as f:
    json.dump(a, f)

