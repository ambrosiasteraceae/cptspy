import sys
import pyqtgraph as pg
import numpy as np
import pandas as pd
import os
from PyQt6.QtWidgets import *
from PyQt6.uic import loadUi
from utility import CustomGrid
from PyQt6.QtGui import QStandardItemModel, QStandardItem, QBrush,QColor

from gui.extras import TreeGridItem
from pyqtgraph import PlotWidget

from datagen import generate_coords, generate_custom_grid, generate_tests
from interactions import GraphButtonHandler
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



    def display_item(self):
        pass

    def repaint_tests(self):
        pass
        objective = self.combo_list_btn.currentText()
        val = self.df[objective].values

        # Create 5 colors for each stop (these are RGB values)

        print(val)
        # Create the colormap
        colormap = pg.colormap.get('cividis')

        normalized = (val - val.min()) / (val.max() - val.min())
        # if objective == "cum_ic":
        #     normalized = val / 2*125
        # elif objective == "cum_fos":
        #     normalized = val / 2*125
        # else:
        #     diff = val.max() - val.min()
        #     normalized = (val - val.min()) / (val.max() - val.min())
        # Get the colors from the colormap
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
        if objective not in ['cum_ic', 'cum_fos']:
            self.color_bar_item.setLabels({f'{min(val)}': 0,
                                           f'{0.25 * diff / val.min()}': 0.25,
                                           f'{0.5 * diff / val.min()}': 0.5,
                                           f'{0.75 * diff / val.min()}': 0.75,
                                           f'{max(val)}': 1})
        else:
            self.color_bar_item.setLabels({f'{min(val)}': 0,
                                           f"{125 if objective == 'cum_ic' else 150}" : 0.5,
                                           f'{max(val)}': 1}
                                          )

        # color_bar_item.showLegend(True)
        self.color_bar_item.setOpacity(0.7)
        self.plot.addItem(self.color_bar_item)
        self.cpts.setBrush(brushes)
        self.plot.update()


    def repaint_tests2(self):
        # Thresholds
        thresh_yellow = 110
        thresh_red = 150

        # Define the color map
        pos = np.array([0.0, 0.5, 1.0])
        color = np.array([[0, 255, 0, 255], [255, 255, 0, 255], [255, 0, 0, 255]], dtype=np.ubyte)
        cmap = pg.ColorMap(pos, color)

        # Normalize values
        objective = self.combo_list_btn.currentText()
        val = self.df[objective].values
        normalized = (val - val.min()) / (val.max() - val.min())

        # Apply color map
        colors = cmap.map(normalized, mode='qcolor')
        print(colors[:10])

        # Adjust colors based on thresholds
        if objective == "cum_ic":
            for i, color in enumerate(colors):
                if val[i] > thresh_red:
                    color.setRed(255)  # make it darker red if it exceeds the red threshold
                elif val[i] > thresh_yellow:
                    color.setRed(255)
                    color.setGreen(255)  # make it yellow if it exceeds the yellow threshold
                else:
                    color.setGreen(255)  # keep it green otherwise

        # Convert colors to brushes
        brushes = [QBrush(color) for color in colors]

        # Apply brushes
        self.cpts.setBrush(brushes)
        self.plot.update()



    def limit_colors(self):

        objective = self.combo_list_btn.currentText()
        val = self.df[objective].values
        limit = 150
        def determine_color(x):
            if x > limit + 100:
                return QColor(191, 0, 0, 255)
            elif limit < x < limit + 50:
                return QColor(242, 0, 0, 255)
            elif limit > x > limit-25:
                return QColor(229, 102, 38, 255)
            else:
                return QColor(26, 153, 26, 255)

        vectorized = np.vectorize(determine_color)

        colors = vectorized(val)

        brushes = [QBrush(color) for color in colors]

        color_map = pg.ColorMap(
            [0, 0.25, 0.5, 0.75, 1],
            [
                QColor(191, 0, 0, 255),
                QColor(242, 0, 0, 255),
                QColor(229, 102, 38, 255),
                QColor(255, 166, 64, 255),
                QColor(26, 153, 26, 255)
            ]
        )

        # Create the color bar item
        color_bar_item = pg.GradientLegend(size=(10, 200), offset=(20, 0))
        color_bar_item.setGradient(color_map.getGradient())

        # color_bar_item.showLegend(True)
        color_bar_item.setOpacity(0.7)
        # Add the color bar to the plot
        self.plot.addItem(color_bar_item)

        # Define label values
        labels = {
            0: '0',
            0.25: str(limit),
            0.5: str(limit + 25),
            0.75: str(limit + 50),
            1: str(limit + 100)
        }

        # Create and add TextItem labels to plot
        # for position, text in labels.items():
        #     label = pg.TextItem(text, anchor=(0, 0.5))
        #     label.setColor('k')
        #     self.plot.addItem(label)
        #     label.setPos(20, position * 200)


        # Apply brushes
        self.cpts.setBrush(brushes)
        self.plot.update()



    def kk(self):
        pass

    # FS_0p50_to_0p75
    # QColor(191, 0, 0, 255)
    # # FS_0p75_to_1p0: (0.95, 0, 0)
    # QColor(242, 0, 0, 255)
    # # FS_1p0_to_1p25: (0.9, 0.4, 0.15, 255)
    # QColor(229, 102, 38, 255)

    # # FS_1p25_to_1p5: (1, 0.65, 0.25, 255)
    # QColor(255, 166, 64, 255)

    # # FS_1p5_to_HIGH: (0.1, 0.6, 0.1, 255)
    # QColor(26, 153, 26, 255)
    # # FS_NON_LIQ: (0.4, 0.4, 0.4)
    # QColor(102, 102, 102)

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

# with open("uis/white_theme.qss", "r") as f:
with open ("C:/Users/dragos/Documents/GitHub/cptspy/gui/uis/white_theme.qss", "r") as f:
    _style = f.read()
    app.setStyleSheet(_style)

main.show()
sys.exit(app.exec())
