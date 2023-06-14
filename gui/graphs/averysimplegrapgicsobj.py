"""
Demonstrates the usage of DateAxisItem to display properly-formatted
timestamps on x-axis which automatically adapt to current zoom level.

"""
from PyQt6.QtWidgets import *
from PyQt6.QtCore import QPointF
from PyQt6.QtGui import QPolygonF

import time
import numpy as np
import pyqtgraph as pg
from shapely import Polygon


def gen_polygon(x, y, l):
    # do this the numpy way
    return Polygon([(x - l, y - l), (x - l, y + l), (x + l, y + l), (x + l, y - l), ])


class MultiPolygonObj(QGraphicsItemGroup):
    def __init__(self):
        super().__init__()

        easting, northing = np.random.random_sample((2, 10000)) * 10000
        ids = np.arange(easting.size)
        colors = ['#ffe3b3', '#53d2dc', '#4f8fc0']
        color_array = np.random.choice(colors, ids.size)
        points = list(zip(easting, northing))
        qpoints = [QPointF(*point) for point in points]

        qpoints_xvals = [point.x() for point in qpoints]
        qpoints_yvals = [point.y() for point in qpoints]

        spots = [{'pos': [qpoints_xvals[i], qpoints_yvals[i]], 'data': ids[i], 'brush': color_array[i]} for i in
                 range(ids.size)]

        cpts = pg.ScatterPlotItem(size=14, symbol='x', pen=pg.mkPen(None), brush=pg.mkBrush(155, 55, 255, 120))
        # cpts.sigClicked.connect(self.clicked)
        cpts.addPoints(spots)
        self.addToGroup(cpts)

        self.grid_polygons = [gen_polygon(*point, 25) for point in points]
        self.graph_bottleneck()


    def graph_bottleneck(self):
        for polygon in self.grid_polygons:
            poly = np.array(polygon.exterior.coords.xy).T
            qpoly = QPolygonF([QPointF(*p) for p in poly])
            grid = QGraphicsPolygonItem(qpoly)
            self.addToGroup(grid)
            grid.setPen(pg.mkPen('black', width=0.2, ))

            # self.plot.addItem(grid)


mm = MultiPolygonObj()
# print(mm.grid_polygons)



app = pg.mkQApp("Polygon Example")

# Create a plot with a date-time axis
w = pg.PlotWidget()
# w.showGrid(x=True, y=True)
w.setBackground('w')

myplot = w.getPlotItem()


myplot.addItem(mm)
# w.setWindowTitle('pyqtgraph example: DateAxisItem')
w.show()

if __name__ == '__main__':
    pg.exec()
