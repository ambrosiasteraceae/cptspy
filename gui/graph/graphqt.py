import sys
import pyqtgraph as pg
import numpy as np
import pandas as pd
import os
from PyQt6.QtWidgets import *
from PyQt6.uic import loadUi
from gui.graph.utility import CustomGrid
from PyQt6.QtGui import QStandardItemModel, QStandardItem, QBrush,QColor

from gui.extras import TreeGridItem
from pyqtgraph import PlotWidget

from gui.graph.datagen import generate_coords, generate_custom_grid, generate_tests
from gui.graph.interactions import GraphButtonHandler
from miscellaneous.plots import create_cpt_9_plot


class GraphQT(QDialog):

    def __init__(self, main_window_ref, parent=None):
        super(GraphQT, self).__init__(parent)
        # loadUi('uis/graph2.ui', self)
        gui_dir_path = os.path.split(os.path.dirname(__file__))[0]  # Get the path to the gui directory
        loadUi(os.path.join(gui_dir_path, 'uis', 'graph2.ui'), self)
        self.main = main_window_ref
        self.plot = self.graph.getPlotItem()


        self.container = {}
        self.lastClicked = []

        self.grids = []
        self.tests = []

        self.graph.setBackground('w')
        self.graph.setAspectLocked(True)
        self.clickedPen = pg.mkPen('r', width=1, cosmetic=True)

        if self.main == 123:
            self.plot_proj()
        else:
            self.plot_btn.clicked.connect(self.plot_proj)






        self.children = self.plot.scene().items()  # child for child in children if isinstance(child, CustomGrid

        self.treemodel = QStandardItemModel()
        self.treemodel.setHorizontalHeaderLabels(['Name', 'Value'])
        self.treeView.setModel(self.treemodel)


        self.cpts.sigClicked.connect(self.clicked)  # TODO SHOULD BE OUTSIDE
        self.handler = GraphButtonHandler(self)

        self.combo_list_btn.addItems(
            ['groundlvl', 'max_fos_elev', 'max_ic_elev', 'min_fos_elev', 'min_ic_elev', 'cum_fos', 'cum_ic', 'min_fos'])
        self.repaint_tests_btn.clicked.connect(self.repaint_tests)
        self.compare_btn.clicked.connect(self.compare)


    def compare(self):
        #QFileSystemModel
        #get all elements of treemodel
        #

        elements = []
        for row in range(self.treemodel.rowCount()):
            for column in range(self.treemodel.columnCount()):
                item = self.treemodel.item(row, column)
                if item is not None:
                    element = item.text()
                    elements.append(element)
                       
        print(elements) 
        from calc.testnpyformat import CPTloader
        #from calc.liquefaction import run_rw1997
        from miscellaneous.plots import create_cpt_9_plot
        #ffp = 'C:/Users/dragos/Documents/GitHub/cptspy/gui/Hudayriyat2/calc/'
        ffp = 'D:/05_Example/biotopia/calc/'
        cpts = []
        for ele in elements:
            f = np.load(ffp + ele + '.npz', allow_pickle= True)
            cpt = CPTloader(f)
            cpts.append(cpt)
        create_cpt_9_plot(cpts)
        #find all items of treemodel


    def repaint_tests(self):
        pass
        objective = self.combo_list_btn.currentText()
        val = self.df[objective].values

        val = np.where(np.isnan(val), 0, val)

        # Create 5 colors for each stop (these are RGB values)

        print(val)
        # Create the colormap
        if objective == "cum_ic" or objective == "cum_fos":
            pos = [0., 0.098, 0.196, 0.294, 0.392, 0.49, 0.5, 0.75, 1]
            colors = [
                (0, 100, 0),  # Dark Green
                (34, 139, 34),  # Forest Green
                (173, 255, 47),  # Green Yellow
                (255, 140, 0),  # Dark Orange
                (255, 165, 0),  # Orange
                (255, 223, 0),  # Gold
                (255, 0, 0),  # Red
                (178, 34, 34),  # Firebrick
                (139, 0, 0),  # Dark Red
            ]
            colormap = pg.ColorMap(pos, colors)
        else:
            colormap = pg.colormap.get('inferno')

        #normalized = (val - val.min()) / (val.max() - val.min())
        if objective == "cum_ic":
            normalized = val / (2*125)
        elif objective == "cum_fos":
            normalized = val / (2*150)
        else:
            diff = val.max() - val.min()
            normalized = (val - val.min()) / (val.max() - val.min())
        for i,x in zip(val[:100], normalized[:100]):
            print(i,x)

        #Get the colors from the colormap
        colors = colormap.map(normalized, mode='byte')

        # Convert colors to QColor objects
        colors = [QColor(*color) for color in colors]

        # Create brushes
        brushes = [QBrush(color) for color in colors]

        try:
            self.plot.removeItem(self.color_bar_item)
        except AttributeError:
            pass

        self.color_bar_item = pg.GradientLegend(size=(10, 200), offset=(20, 50))

        self.color_bar_item.setGradient(colormap.getGradient())
        diff = val.max() - val.min()
        valmin = val.min() if val.min() != 0 else 1
        if objective not in ['cum_ic', 'cum_fos']:
            self.color_bar_item.setLabels({f'{min(val)}': 0,
                                           f'{0.25 * diff / valmin}': 0.25,
                                           f'{0.5 * diff / valmin}': 0.5,
                                           f'{0.75 * diff / valmin}': 0.75,
                                           f'{max(val)}': 1})
        else:
            self.color_bar_item.setLabels({f'{min(val)}': 0,
                                           f"{125 if objective == 'cum_ic' else 150}" : 0.5,
                                           f'{max(val)}': 1}
                                          )

        # color_bar_item.showLegend(True)
        self.color_bar_item.setOpacity(0.7)
        self.plot.addItem(self.color_bar_item)

        # self.cpts.setBrush(brushes)
        print(len(self.points), len(self.ids))
        spots = [{'pos': [*self.points[i]], 'data': val[i], 'brush':brushes[i]} for i in
             range(self.ids.size)]
        self.cpts.clear()
        self.cpts.addPoints(spots)
        self.plot.update()

    def fill_check_manager_analysis(self):
        # so the idea is that we wwill have 3 checkboxes
        # 1. liquefaction
        # 2. i_c
        # 3. bearing capacity
        # 4. settlement

        pass


    def locate_grid(self, grid):
        for child in self.children:
            if isinstance(child, CustomGrid):
                if child.name == grid:
                    return child
        return None


    def plot_proj(self):
        self.points, self.ids, self.df= generate_coords(self) #could be only self.main
        self.cpts = generate_tests(self.points, self.ids)

        self.grid_group = generate_custom_grid(self, self.points, self.ids, self.df)
        self.plot.addItem(self.grid_group)
        self.plot.addItem(self.cpts)
        self.ungroup()
        self.plot.setXRange(self.df['Easting'].min(), self.df['Easting'].max())
        self.plot.setYRange(self.df['Northing'].min(), self.df['Northing'].max())

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


    def ungroup(self):
        # Get all the child items in the group
        items = self.grid_group.childItems()
        # Remove each item from the group
        for item in items:
            self.grid_group.removeFromGroup(item)



    def insert_grid(self, _grid):
        self.treemodel.appendRow(TreeGridItem(_grid).parent)


app = QApplication(sys.argv)
main = GraphQT(123)

path = 'D:/04_R&D/cptspy/gui/uis/white_theme.qss' #work
#path = "C:/Users/dragos/Documents/GitHub/cptspy/gui/uis/white_theme.qss" #home
# with open("uis/white_theme.qss", "r") as f:
with open (path, "r") as f:
    _style = f.read()
    app.setStyleSheet(_style)

main.show()
sys.exit(app.exec())
