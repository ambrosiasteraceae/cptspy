from PyQt6.QtWidgets import *
from PyQt6.QtCore import QPointF
from PyQt6.QtGui import QPolygonF, QBrush
from PyQt6.QtCore import Qt
import time
import numpy as np
import pyqtgraph as pg
from shapely import Polygon



class SelectablePolygonItem(QGraphicsPolygonItem):
    def __init__(self, polygon):
        super().__init__(polygon)

        self.setAcceptHoverEvents(True)

        self.setFlags(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable |
                  QGraphicsItem.GraphicsItemFlag.ItemIsMovable |
                  QGraphicsItem.GraphicsItemFlag.ItemIsFocusable)

    def setSelected(self, selected):
        super().setSelected(selected)
        print('yes')
        if selected:
            self.setBrush(QBrush(Qt.GlobalColor.red))  # fill color when selected
        else:
            self.setBrush(QBrush(Qt.GlobalColor.yellow))  # default color when deselected

def gen_polygon(x, y, l):
    # do this the numpy way
    return Polygon([(x - l, y - l), (x - l, y + l), (x + l, y + l), (x + l, y - l), ])


class MultiPolygonObj(QGraphicsItemGroup):
    def __init__(self):
        super().__init__()
        self.lastClicked = []
        easting, northing = np.random.random_sample((2, 3500)) * 10000
        ids = np.arange(easting.size)
        colors = ['#ffe3b3', '#53d2dc', '#4f8fc0']
        color_array = np.random.choice(colors, ids.size)
        points = list(zip(easting, northing))
        qpoints = [QPointF(*point) for point in points]
        self.clickedPen = pg.mkPen('r', width=1, cosmetic=True)
        qpoints_xvals = [point.x() for point in qpoints]
        qpoints_yvals = [point.y() for point in qpoints]

        spots = [{'pos': [qpoints_xvals[i], qpoints_yvals[i]], 'data': ids[i], 'brush': color_array[i]} for i in
                 range(ids.size)]

        cpts = pg.ScatterPlotItem(size=14, symbol='x', pen=pg.mkPen(None), brush=pg.mkBrush(155, 55, 255, 120))
        cpts.sigClicked.connect(self.clicked)
        print('CPTS graph is of tyep : ',type(cpts))

        cpts.addPoints(spots)
        self.addToGroup(cpts)

        self.grid_polygons = [gen_polygon(*point, 25) for point in points]
        self.graph_bottleneck()

    def clicked(self, plot, points):
        for p in self.lastClicked:
            p.resetPen()
        # print("Clicked points:", points)
        print(points[0].data())

        # Store the selected points
        self.lastClicked.extend(points)

        for p in self.lastClicked:
            p.setPen(self.clickedPen)
        print('MyList', [s.data() for s in self.lastClicked])

    def graph_bottleneck(self):
        for polygon in self.grid_polygons:
            poly = np.array(polygon.exterior.coords.xy).T
            qpoly = QPolygonF([QPointF(*p) for p in poly])
            grid = SelectablePolygonItem(qpoly)
            grid.setPen(pg.mkPen('black', width=0.2, ))


            # selectable_grid = SelectablePolygonItem(qpoly)
            self.addToGroup(grid)

            # self.plot.addItem(grid)


mm = MultiPolygonObj()
app = pg.mkQApp("Polygon Example")
w = pg.PlotWidget()
w.setBackground('w')
myplot = w.getPlotItem()
myplot.addItem(mm)

w.show()

if __name__ == '__main__':
    pg.exec()