from PyQt6.QtWidgets import *
from PyQt6.uic import loadUi
import sys
from pyqtgraph import PlotWidget
import pandas as pd
import pyqtgraph as pg
import numpy as np
from shapely import Polygon
path = 'D:/05_Example/Hudayriyat/summary/Results.xlsx'


class HomeQT2(QDialog):
    def __init__(self, main_window_ref, parent=None):
        super(HomeQT2, self).__init__(parent)
        # loadUi('uis/home2.ui', self)
        # loadUi('uis/convert2.ui', self)
        # loadUi('uis/projreqs2.ui', self)

        # loadUi('uis/load2.ui', self)
        # loadUi('uis/calculations2.ui', self)
        # loadUi('uis/overview2.ui', self)
        loadUi('uis/graph2.ui', self)

        self.main = main_window_ref

        df = pd.read_excel(path)
        df['Northing'] = df['Northing'].astype(float)
        df['Easting'] = df['Easting'].astype(float)
        northing = df['Northing'].values
        easting = df['Easting'].values
        ids = df['CPT-ID'].values

        colors = ['#ffe3b3', '#53d2dc', '#4f8fc0']
        color_array = np.random.choice(colors, ids.size)

        contrasting_colors = ['#10367a', '#db4c0c', '#f1c40f']
        color_contrast_array = np.random.choice(contrasting_colors, ids.size)


        self.graph.setBackground('w')

        self.clickedPen = pg.mkPen('r', width=1, cosmetic=True)
        self.lastClicked = []

        plot_item = self.graph.getPlotItem()

        self.hoverPen = pg.mkPen(color='yellow', width=2)

        s1 = pg.ScatterPlotItem(size=15, pen=pg.mkPen(None), brush=pg.mkBrush(155, 55, 255, 120))

        spots2 = [{'pos': [easting[i]+25, northing[i]+25], 'data': ids[i], 'brush': color_contrast_array[i]} for i in range(ids.size)]
        spots = [{'pos': [easting[i], northing[i]], 'data': ids[i], 'brush': color_array[i]} for i in range(ids.size)]
        s1.addPoints(spots)
        s1.addPoints(spots2)
        s1.sigClicked.connect(self.clicked)
        s1.sigHovered.connect(self.hovered)
        plot_item.addItem(s1)


        width = 20
        data_points =  list(zip(easting, northing))
        rectangles = [Polygon([(x, y), (x + width, y), (x + width, y + width), (x, y + width)]) for x, y in data_points]

        poly = rectangles[0]

        coords_x = np.array([x[0] for x in poly.exterior.coords])
        coords_y =  np.array([x[1] for x in poly.exterior.coords])

        z = np.random.normal(size=(len(coords_x), len(coords_y)))

        s2 = pg.PColorMeshItem(coords_x, coords_y,z)
        plot_item.addItem(s2)


    def clicked(self, plot, points):
            for p in self.lastClicked:
                p.resetPen()
            print("Clicked points:", points)
            print(points[0].data())

            # Store the selected points
            self.lastClicked.extend(points)

            for p in self.lastClicked:
                p.setPen(self.clickedPen)
            # print('MyList',[s.data() for s in self.lastClicked])

    def hovered(self, plot, points):
        print("Hovered points:", points)
        for p in points:
            p.setPen(pg.mkPen(color='y', width=2))  # Set a yellow pen for the hovered points
            print(p.data())
        self.plot_item.update()  # Update the plot to reflect the changes


app = QApplication(sys.argv)
main = HomeQT2(123)

with open("uis/white_theme.qss", "r") as f:
    _style = f.read()
    app.setStyleSheet(_style)

main.show()
sys.exit(app.exec())


############## ROI ############
# self.selectionROI = pg.RectROI([0, 0], [1, 1], pen=(255, 0, 0, 100))
# self.selectionROI.setZValue(10)  # Make sure it's on top of other items
# self.graph.addItem(self.selectionROI)
# # Connect the selectionChanged signal of ROI to the selectionChanged slot
# self.selectionROI.sigRegionChanged.connect(self.selectionChanged)
#
#
# def selectionChanged(self):
#     # Get the position and size of the selection ROI
#     pos = self.selectionROI.pos()
#     size = self.selectionROI.size()
#
#     # Calculate the bounding rectangle
#     rect = pg.QtCore.QRectF(pos, size)
#
#     # Check which points are inside the selection rectangle
#     selected_points = []
#     scatter_item = self.graph.listDataItems()[0]  # Get the ScatterPlotItem
#     for point in scatter_item.points():
#         if rect.contains(*point.pos()):
#             selected_points.append(point)
#
#     # Perform actions on the selected points
#     for point in selected_points:
#         # Do something with the selected points
#         print("Selected point:", point.pos())
