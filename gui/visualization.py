import sys
import pyqtgraph as pg
import numpy as np
import pandas as pd
from PyQt6.QtWidgets import *
from PyQt6.uic import loadUi
from PyQt6.QtCore import QPointF
from PyQt6.QtGui import QPolygonF, QFont
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from shapely import Polygon
from extras import Test, Grid, TreeGridItem
from pyqtgraph import PlotWidget
from rtree import index

def gen_polygon(x, y, l):
    return Polygon([(x - l, y - l), (x - l, y + l), (x + l, y + l), (x + l, y - l), ])


class CustomGrid(QGraphicsPolygonItem):
    def __init__(self, *args, graph_ref, gridobj, **kwargs):
        super().__init__(*args, **kwargs)
        # self.setAcceptHoverEvents(True)
        self.graph = graph_ref
        self.grid_obj = gridobj

    def hoverEnterEvent(self, event):
        print('Mouse entered at: ', event.screenPos(), self.grid_obj)

    def mousePressEvent(self, event):
        self.setBrush(pg.mkBrush(0, 255, 0, 100))
        self.graph.container[self.grid_obj.name] = self.polygon()
        print(len(self.graph.container))
        # super().mousePressEvent(event)
        print('Bounding area: ', self.polygon().boundingRect())
        self.graph.insert_grid(self.grid_obj)


class GraphQT(QDialog):

    def __init__(self, main_window_ref, parent=None):
        super(GraphQT, self).__init__(parent)
        loadUi('uis/graph2.ui', self)
        self.main = main_window_ref
        self.plot = self.graph.getPlotItem()

        self.container = {}
        self.lastClicked = []

        self.grids =[]
        self.tests = []

        self.graph.setBackground('w')
        self.graph.setAspectLocked(True)
        self.clickedPen = pg.mkPen('r', width=1, cosmetic=True)

        if self.main == 123:
            self.plot_proj()
        else:
            self.plot_btn.clicked.connect(self.plot_proj)
            # self.plot.setXRange(self.df['Easting'].min(), self.df['Easting'].max())
            # self.plot.setYRange(self.df['Northing'].min(), self.df['Northing'].max())

        self.children = self.plot.scene().items()  # child for child in children if isinstance(child, CustomGrid

        self.treemodel = QStandardItemModel()
        self.treemodel.setHorizontalHeaderLabels(['Name', 'Value'])
        self.treeView.setModel(self.treemodel)

        self.color_grids_btn.clicked.connect(self.color_grids)
        self.refresh_grid_color_btn.clicked.connect(self.refresh_grid_color)
        self.grid_btn.setChecked(True)
        self.grid_btn.stateChanged.connect(self.gridstate)

        self.test_btn.setChecked(True)
        self.test_btn.stateChanged.connect(self.teststate)

        self.grid_passing_btn.clicked.connect(self.grid_passing)


    def fill_check_manager_analysis(self):
        #so the idea is that we wwill have 3 checkboxes
        #1. liquefaction
        #2. i_c
        #3. bearing capacity
        #4. settlement


        pass

    def grid_passing(self):
        print('Btnclicked')
        for child in self.children:
            if isinstance(child, CustomGrid):
                i_c_limit = 150
                fos_limit = 150
                for test in child.grid_obj.tests:
                    if test.cum_ic >= i_c_limit:
                        child.setBrush(pg.mkBrush(255, 0, 0, 100)) #red
                        break
                    child.setBrush(pg.mkBrush(0, 0, 255, 100)) #blue
        self.plot.update()


    def locate_grid(self, grid):
        for child in self.children:
            if isinstance(child, CustomGrid):
                if child.name == grid:
                    return child
        return None

    def teststate(self):
        if self.test_btn.isChecked() == True:
            self.see_scatter()
        else:
            self.hide_scatter()


    def gridstate(self):
        if self.grid_btn.isChecked() == True:
            self.see_grids()
        else:
            self.hide_grids()

    def see_scatter(self):
        for child in self.children:
            if isinstance(child, pg.ScatterPlotItem):
                child.show()

    def see_grids(self):
        for child in self.children:
            if isinstance(child, CustomGrid):
                child.show()

    def hide_grids(self):
        for child in self.children:
            if isinstance(child, CustomGrid):
                child.hide()
    def hide_scatter(self):
        for child in self.children:
            if isinstance(child, pg.ScatterPlotItem):
                child.hide()


    def refresh_grid_color(self):
        for child in self.children:
            if isinstance(child, CustomGrid):
                # Set color to white green
                # child.setBrush(pg.mkBrush(255, 0, 0, 100))
                child.setPen(pg.mkPen('black', width=0.5, ))
                child.setBrush(pg.mkBrush(None))

    def color_grids(self):
        for child in self.children:
            if isinstance(child, CustomGrid):
                #Set color to white green
                child.setBrush(pg.mkBrush(255, 0, 0, 100))
                # child.setBrush(pg.mkBrush(255, 255, 255, 100))


    def plot_proj(self):
        self.points, self.ids = self.generate_coords()
        cpts = self.generate_tests()
        self.generate_grid()
        self.plot.addItem(self.grid_group)
        self.plot.addItem(cpts)
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
        labels = []
        def add_labels():
            for spot in spots:
                label = pg.TextItem(text=str(spot['data']), color=(0, 0, 0))
                label.setPos(spot['pos'][0], spot['pos'][1] + 5)  # Adjust the label position as desired
                # self.plot.addItem(label)
                # label.setScale(1)
                labels.append(label)
            for label in labels:
                self.plot.addItem(label)
        # add_labels()

        cpts.addPoints(spots)
        return cpts


    def map_grids_to_tests(self):
        grid_names = [s.split('_')[1][:-1] for s in self.ids]
        multipolygon = [gen_polygon(x, y, 15) for x, y in self.points]
        list_of_df_records = self.df.to_dict('records')
        grids = [Grid(name, poly.bounds, poly, set(), []) for name, poly in zip(grid_names, multipolygon)]
        tests = [Test(**d) for d in list_of_df_records]

        rtree = index.Index()
        for i, test in enumerate(tests):
            rtree.insert(i, (test.Easting, test.Northing, test.Easting, test.Northing), obj=test)

        for grid in grids:
            found_tests = list(rtree.intersection(grid.bounds, objects=True))
            # print([t.object for t in found_tests])
            for test in found_tests:
                grid.insert(test.object)
        return grids

    def generate_grid(self):
        self.grids = self.map_grids_to_tests()
        # grid_polygons = [gen_polygon(*point, 25) for point in self.points]
        gridItems = []
        for grid in self.grids:
            poly = np.array(grid.polygon.exterior.coords.xy).T
            qpoly = QPolygonF([QPointF(*p) for p in poly])
            gridItem = CustomGrid(qpoly, graph_ref=self, gridobj=grid)
            gridItem.setPen(pg.mkPen('black', width=0.5, ))
            gridItems.append(gridItem)
        self.grid_group = QGraphicsItemGroup()
        [self.grid_group.addToGroup(grid) for grid in gridItems]

    def ungroup(self):
        # Get all the child items in the group
        items = self.grid_group.childItems()
        # Remove each item from the group
        for item in items:
            self.grid_group.removeFromGroup(item)



    def generate_coords(self):
        if self.main == 123:
            # self.df =pd.read_excel('D:/05_Example/Hudayriyat/summary/Results.xlsx')
            self.df =pd.read_excel('C:/Users/dragos/Documents/GitHub/cptspy/gui/hudayriyat/summary/Results.xlsx')
        else:
            self.df = pd.read_excel(self.main.ffp.summary + 'Results.xlsx')
        self.df['Northing'] = self.df['Northing'].astype(float)
        self.df['Easting'] = self.df['Easting'].astype(float)
        northing = self.df['Northing'].values
        easting = self.df['Easting'].values
        ids = self.df['Name'].values
        points = list(zip(easting, northing))
        return points, ids

    def insert_grid(self, _grid):
        self.treemodel.appendRow(TreeGridItem(_grid).parent)


# from graph.graphqt import GraphQT



app = QApplication(sys.argv)
main = GraphQT(123)

with open("uis/white_theme.qss", "r") as f:
    _style = f.read()
    app.setStyleSheet(_style)

main.show()
sys.exit(app.exec())

