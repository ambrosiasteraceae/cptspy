import sys
import pyqtgraph as pg
import numpy as np
import pandas as pd
from PyQt6.QtWidgets import *
from PyQt6.uic import loadUi
from PyQt6.QtCore import QPointF
from PyQt6.QtGui import QPolygonF
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from shapely import Polygon
from extras import Test,Grid,TreeGridItem
from pyqtgraph import PlotWidget




def gen_polygon(x, y, l):
    return Polygon([(x - l, y - l), (x - l, y + l), (x + l, y + l), (x + l, y - l), ])


class CustomPolygonItem(QGraphicsPolygonItem):
    def __init__(self, *args, graph_ref, id_number, **kwargs):
        super().__init__(*args, **kwargs)
        # self.setAcceptHoverEvents(True)
        self.graph = graph_ref
        self.name = id_number

    def hoverEnterEvent(self, event):
        print('Mouse entered at: ', event.screenPos(), self.name)

    def mousePressEvent(self, event):
        self.setBrush(pg.mkBrush(255, 0, 0, 100))
        self.graph.container[self.name] = self.polygon()
        print(len(self.graph.container))
        # super().mousePressEvent(event)

        grid = Grid('AK47', (1, 1), [Test('AK47-1a', 1, 1, 1, 1, 1, None)])
        grid.insert(Test('AK47-1b', 1, 1, 1, 1, 1, None))
        self.graph.insert_grid(grid)





class GraphQT(QDialog):

    def __init__(self, main_window_ref, parent=None):
        super(GraphQT, self).__init__(parent)
        loadUi('uis/graph2.ui', self)
        self.main = main_window_ref
        self.plot = self.graph.getPlotItem()

        self.container = {}
        self.lastClicked = []
        self.points, self.ids = self.generate_coords()

        self.graph.setBackground('w')
        self.graph.setAspectLocked(True)
        self.clickedPen = pg.mkPen('r', width=1, cosmetic=True)


        cpts = self.generate_scatter()
        self.generate_grid()

        children = self.plot.scene().items()  # child for child in children if isinstance(child, CustomPolygonItem

        self.plot.addItem(self.grid_group)
        self.plot.addItem(cpts)


        self.treemodel = QStandardItemModel()
        self.treemodel.setHorizontalHeaderLabels(['Name', 'Value'])
        self.treeView.setModel(self.treemodel)


        self.ungroup()

    def clicked(self, plot, points):
        for p in self.lastClicked:
            p.resetPen()
        print(points[0].data())
        self.lastClicked.extend(points)

        for p in self.lastClicked:
            p.setPen(self.clickedPen)
        print('MyList', [s.data() for s in self.lastClicked])

    def hovered(self, plot, points):
        print("Hovered points:", points)
        for p in points:
            p.setPen(pg.mkPen(color='y', width=2))
            print(p.data())
        self.plot.update()

    def generate_scatter(self):
        "Benchmark Test Function"
        easting, northing = np.random.random_sample((2, 20000)) * 10000
        self.points = list(zip(easting, northing))
        ids = np.arange(easting.size)
        colors = ['#ffe3b3', '#53d2dc', '#4f8fc0']
        color_array = np.random.choice(colors, ids.size)
        cpts = pg.ScatterPlotItem(size=12, symbol='x', pen=pg.mkPen(None), brush=pg.mkBrush(155, 55, 255, 120))
        cpts.sigClicked.connect(self.clicked)
        spots = [{'pos': [*self.points[i]], 'data': ids[i], 'brush': color_array[i]} for i in
                 range(ids.size)]
        cpts.addPoints(spots)
        return cpts


    def generate_tests(self):
        # easting, northing = np.random.random_sample((2, 20000)) * 10000
        # self.points = list(zip(easting, northing))
        # ids = np.arange(easting.size)
        colors = ['#ffe3b3', '#53d2dc', '#4f8fc0']
        color_array = np.random.choice(colors, self.ids.size)
        cpts = pg.ScatterPlotItem(size=12, symbol='x', pen=pg.mkPen(None), brush=pg.mkBrush(155, 55, 255, 120))
        cpts.sigClicked.connect(self.clicked)
        spots = [{'pos': [*self.points[i]], 'data': self.ids[i], 'brush': color_array[i]} for i in
                 range(self.ids.size)]
        cpts.addPoints(spots)
        return cpts

    def generate_grid(self):
        all_grids = []
        grid_polygons = [gen_polygon(*point, 25) for point in self.points]
        for i, polygon in enumerate(grid_polygons):
            poly = np.array(polygon.exterior.coords.xy).T
            qpoly = QPolygonF([QPointF(*p) for p in poly])
            grid = CustomPolygonItem(qpoly, graph_ref=self, id_number=i)
            grid.setPen(pg.mkPen('black', width=0.5, ))
            all_grids.append(grid)
        self.grid_group = QGraphicsItemGroup()
        [self.grid_group.addToGroup(grid) for grid in all_grids]

    def ungroup(self):
        # Get all the child items in the group
        items = self.grid_group.childItems()

        # Remove each item from the group
        for item in items:
            self.grid_group.removeFromGroup(item)

    def generate_coords(self):
        df = pd.read_excel(self.main.ffp.summary + 'Results.xlsx')
        df['Northing'] = df['Northing'].astype(float)
        df['Easting'] = df['Easting'].astype(float)
        northing = df['Northing'].values
        easting = df['Easting'].values
        ids = df['CPT-ID'].values
        points = list(zip(easting, northing))
        return points, ids



    def insert_grid(self,_grid):
        self.treemodel.appendRow(TreeGridItem(_grid).parent)






# app = QApplication(sys.argv)
# main = GraphQT(123)
#
# with open("uis/white_theme.qss", "r") as f:
#     _style = f.read()
#     app.setStyleSheet(_style)
#
# main.show()
# sys.exit(app.exec())
