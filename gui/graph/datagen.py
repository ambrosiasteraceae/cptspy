import pandas as pd
import numpy as np
from shapely import Polygon
from gui.extras import Test, Grid
from PyQt6.QtWidgets import *
from shapely import Polygon
from rtree import index
from PyQt6.QtCore import QPointF
from PyQt6.QtGui import QPolygonF, QFont
from utility import CustomGrid
import pyqtgraph as pg

def gen_polygon(x, y, l):
    return Polygon([(x - l, y - l), (x - l, y + l), (x + l, y + l), (x + l, y - l), ])



def generate_coords(graphqt):
    if graphqt.main == 123:
        # self.df =pd.read_excel('D:/05_Example/Hudayriyat/summary/Results.xlsx')
        df = pd.read_excel('C:/Users/dragos/Documents/GitHub/cptspy/gui/Hudayriyat2/summary/Results.xlsx')
    else:
        df = pd.read_excel(graphqt.main.ffp.summary + 'Results.xlsx')
        df = graphqt.main.df # TODO Later add this
    df['Northing'] = df['Northing'].astype(float)
    df['Easting'] = df['Easting'].astype(float)
    # df[df['Northing', 'Easting']] = df[['Northing', 'Easting']].astype(float)
    ids = df['Name'].values
    points = list(zip(df['Easting'], df['Northing']))
    return points, ids, df

def generate_custom_grid(graphqt, points, ids, df):
    grids = map_grids_to_tests(points, ids, df)
    # grid_polygons = [gen_polygon(*point, 25) for point in self.points]
    gridItems = []
    for grid in grids:
        poly = np.array(grid.polygon.exterior.coords.xy).T
        qpoly = QPolygonF([QPointF(*p) for p in poly])
        gridItem = CustomGrid(qpoly, graph_ref=graphqt, gridobj=grid)
        gridItem.setPen(pg.mkPen('black', width=0.5, ))
        gridItems.append(gridItem)
    grid_group = QGraphicsItemGroup()
    [grid_group.addToGroup(grid) for grid in gridItems]
    return grid_group


def map_grids_to_tests(points, ids, df):
    grid_names = [s for s in ids]
    multipolygon = [gen_polygon(x, y, 15) for x, y in points]
    list_of_df_records = df.to_dict('records')
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


def generate_tests(points,ids):
    # easting, northing = np.random.random_sample((2, 20000)) * 10000
    # points = list(zip(easting, northing))
    # ids = np.arange(easting.size)
    colors = ['#ffe3b3', '#53d2dc', '#4f8fc0']
    color_array = np.random.choice(colors, ids.size)
    cpts = pg.ScatterPlotItem(size=16, symbol='o', pen=pg.mkPen(None), brush=pg.mkBrush(155, 55, 255, 120))


    spots = [{'pos': [*points[i]], 'data': ids[i], 'brush': color_array[i]} for i in
             range(ids.size)]
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



def generate_scatter(self):
    "Benchmark Test Function"
    easting, northing = np.random.random_sample((2, 20000)) * 10000
    self.points = list(zip(easting, northing))
    ids = np.arange(easting.size)
    colors = ['#ffe3b3', '#53d2dc', '#4f8fc0']
    color_array = np.random.choice(colors, ids.size)
    cpts = pg.ScatterPlotItem(size=16, symbol='o', pen=pg.mkPen(None), brush=pg.mkBrush(155, 55, 255, 120))
    cpts.sigClicked.connect(self.clicked)
    spots = [{'pos': [*self.points[i]], 'data': ids[i], 'brush': color_array[i]} for i in
             range(ids.size)]
    cpts.addPoints(spots)
    return cpts
