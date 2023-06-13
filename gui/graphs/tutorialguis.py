from PyQt6 import QtWidgets
import pyqtgraph as pg
import numpy as np
from shapely import Polygon
import pandas as pd




class CustomPlotItem(pg.PlotDataItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.setClickable(True)

    def mouseClickEvent(self, event):
        if self.mouseShape().contains(event.pos()):
            print('Clicked on item with data:', self.getData())
            # calculate which cell was clicked and display its data
            # ...


def on_region_change_finished():
    pass


# calculate which grid cells and CPTs are within the ROI
# ...


path = 'C:/Users/dragos/Documents/GitHub/cptspy/gui/hudayriyat/summary/Results.xlsx'

df = pd.read_excel(path)
df['Northing'] = df['Northing'].astype(float)
df['Easting'] = df['Easting'].astype(float)
northing = df['Northing'].values
easting = df['Easting'].values
ids = df['CPT-ID'].values
points = list(zip(northing,easting))





app = QtWidgets.QApplication([])

# this is your main window
win = QtWidgets.QMainWindow()
win.setWindowTitle('CPT Visualization')

#set white background
pg.setConfigOption('background', 'w')

# create a widget to hold your plot and add it to the main window
widget = QtWidgets.QWidget()
win.setCentralWidget(widget)

# set up the layout for your widget
layout = QtWidgets.QVBoxLayout()
widget.setLayout(layout)

# create a plot widget and add it to your layout
plot_widget = pg.PlotWidget()
layout.addWidget(plot_widget)

# grid_data is a list of polygons where each polygon is a grid cell
# a polygon is a list of tuples where each tuple is a (x, y) coordinate
# grid_data = [np.random.rand(4, 2) * np.array([25, 200]) for _ in range(10)]


grid_polygons = []


def gen_polygon(x, y, l):
    return Polygon([(x - l, y - l), (x - l, y + l), (x + l, y + l), (x + l, y - l)])


grid_polygons = [gen_polygon(*point, 25) for point in points]



for polygon in grid_polygons:
    poly = np.array(polygon.exterior.coords.xy)
    item = CustomPlotItem(poly[0, :], poly[1, :])
    plot_widget.addItem(item)


cpt_data = points
cpt_item = pg.ScatterPlotItem(pos=cpt_data, size=7, symbol='o', brush='b')
plot_widget.addItem(cpt_item)



win.show()
app.exec()
