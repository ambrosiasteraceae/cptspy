from PyQt6.QtWidgets import *
from PyQt6.uic import loadUi
import sys
from pyqtgraph import PlotWidget
import pandas as pd
import pyqtgraph as pg
import numpy as np

from shapely import Polygon
from PyQt6.QtCore import QPointF
from PyQt6.QtGui import QPolygonF


# TODO: Radio button for waht you want to select CPT | Grid


def generate_coords(path):
    df = pd.read_excel(path)
    df['Northing'] = df['Northing'].astype(float)
    df['Easting'] = df['Easting'].astype(float)
    northing = df['Northing'].values
    easting = df['Easting'].values
    ids = df['Name'].values
    return easting, northing, ids


def gen_polygon(x, y, l):
    # do this the numpy way
    return Polygon([(x - l, y - l), (x - l, y + l), (x + l, y + l), (x + l, y - l), ])


class CustomPolygonItem(QGraphicsPolygonItem):
    last_clicked_item = None

    def __init__(self, *args, graph_ref, **kwargs):
        super().__init__(*args, **kwargs)
        # self.setAcceptHoverEvents(True)
        # self.setPen(pg.mkPen('b', width=2))
        self.graph = graph_ref
        self.list = []
        self.last_clicked_item = None

    def hoverEnterEvent(self, event):
        print('Mouse entered at: ', event.screenPos())

    def mousePressEvent(self, event):
        # print('Clicked on item with coordinates:', self.polygon())
        # if CustomPolygonItem.last_clicked_item:
        #     CustomPolygonItem.last_clicked_item.setPen(pg.mkPen('black', width=1))
        # self.setPen(pg.mkPen('r', width=1))
        self.setBrush(pg.mkBrush(255, 0, 0, 100))
        CustomPolygonItem.last_clicked_item = self

        self.graph.container.append(self.polygon())
        print(len(self.graph.container))

        # print('Lenght of my objs: ', len(self.list))
        super().mousePressEvent(event)


class GraphQT(QDialog):
    def __init__(self, main_window_ref, parent=None):
        super(GraphQT, self).__init__(parent)
        # loadUi('uis/home2.ui', self)
        # loadUi('uis/convert2.ui', self)
        # loadUi('uis/projreqs2.ui', self)

        # loadUi('uis/load2.ui', self)
        # loadUi('uis/calculations2.ui', self)
        # loadUi('uis/overv iew2.ui', self)
        loadUi('uis/graph2.ui', self)

        self.main = main_window_ref

        self.container = []

        path = 'D:/05_Example/Hudayriyat/summary/Results.xlsx'
        easting, northing, ids = generate_coords(path)

        colors = ['#ffe3b3', '#53d2dc', '#4f8fc0']
        color_array = np.random.choice(colors, ids.size)

        contrasting_colors = ['#10367a', '#db4c0c', '#f1c40f']
        color_contrast_array = np.random.choice(contrasting_colors, ids.size)

        self.graph.setBackground('w')
        self.clickedPen = pg.mkPen('r', width=1, cosmetic=True)
        self.lastClicked = []

        self.plot = self.graph.getPlotItem()

        self.hoverPen = pg.mkPen(color='yellow', width=2)

        cpts = pg.ScatterPlotItem(size=12, symbol='x', pen=pg.mkPen(None), brush=pg.mkBrush(155, 55, 255, 120))

        cpts.sigClicked.connect(self.clicked)

        self.plot.addItem(cpts)
        self.plot.setAspectLocked(True)
        points = list(zip(easting, northing))

        qpoints = [QPointF(*point) for point in points]

        qpoints_xvals = [point.x() for point in qpoints]
        qpoints_yvals = [point.y() for point in qpoints]

        spots = [{'pos': [qpoints_xvals[i], qpoints_yvals[i]], 'data': ids[i], 'brush': color_array[i]} for i in
                 range(ids.size)]
        cpts.addPoints(spots)

        grid_polygons = [gen_polygon(*point, 25) for point in points]

        all_grids = []
        for polygon in grid_polygons:
            poly = np.array(polygon.exterior.coords.xy).T
            qpoly = QPolygonF([QPointF(*p) for p in poly])
            grid = CustomPolygonItem(qpoly, graph_ref=self)
            grid.setPen(pg.mkPen('black', width=0.5, ))
            all_grids.append(grid)
        grouped_grids
        [self.plot.addItem(grid) for grid in all_grids]

        self.plot.update()
        # self.plot.addItem(QPointF(*points[0]))

    def clicked(self, plot, points):
        for p in self.lastClicked:
            p.resetPen()
        # print("Clicked points:", points)
        print(points[0].data())

        # Store the selected points
        self.lastClicked.extend(points)

        for p in self.lastClicked:
            p.setPen(self.clickedPen)
        print('MyList',[s.data() for s in self.lastClicked])

    def hovered(self, plot, points):
        # s1.sigHovered.connect(self.hovered)

        print("Hovered points:", points)
        for p in points:
            p.setPen(pg.mkPen(color='y', width=2))  # Set a yellow pen for the hovered points
            print(p.data())
        self.self.plot.update()  # Update the plot to reflect the changes

# #
# app = QApplication(sys.argv)
# main = GraphQT(123)
#
# with open("uis/white_theme.qss", "r") as f:
#     _style = f.read()
#     app.setStyleSheet(_style)
#
# main.show()
# sys.exit(app.exec())
