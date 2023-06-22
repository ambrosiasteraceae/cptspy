from PyQt6 import QtCore
import pyqtgraph as pg
from gui.graph.utility import CustomGrid



class GraphButtonHandler:
    def __init__(self, graphqt):
        self.graphqt = graphqt

        # Connect button signals to methods
        self.graphqt.color_grids_btn.clicked.connect(self.color_grids)
        self.graphqt.refresh_grid_color_btn.clicked.connect(self.refresh_grid_color)
        self.graphqt.grid_btn.stateChanged.connect(self.gridstate)
        self.graphqt.test_btn.stateChanged.connect(self.teststate)
        self.graphqt.grid_passing_btn.clicked.connect(self.grid_passing)
        self.graphqt.grid_btn.setChecked(True)
        self.graphqt.test_btn.setChecked(True)

    def color_grids(self):
        for child in self.graphqt.children:
            if isinstance(child, CustomGrid):
                # Set color to white green
                child.setBrush(pg.mkBrush(255, 0, 0, 100))

    def refresh_grid_color(self):
        for child in self.graphqt.children:
            if isinstance(child, CustomGrid):
                # Set color to white green
                child.setPen(pg.mkPen('black', width=0.5, ))
                child.setBrush(pg.mkBrush(None))

    def gridstate(self):
        if self.graphqt.grid_btn.isChecked() == True:
            self.see_grids()
        else:
            self.hide_grids()

    def teststate(self):
        if self.graphqt.test_btn.isChecked() == True:
            self.see_scatter()
        else:
            self.hide_scatter()

    def grid_passing(self):
        print('Btnclicked')
        for child in self.graphqt.children:
            if isinstance(child, CustomGrid):
                i_c_limit = 150
                fos_limit = 150
                for test in child.grid_obj.tests:
                    if test.cum_fos >= i_c_limit:
                        child.setBrush(pg.mkBrush(255, 0, 0, 100))  # red
                        break
                    child.setBrush(pg.mkBrush(0, 0, 255, 100))  # blue
        self.graphqt.plot.update()

    def see_scatter(self):
        for child in self.graphqt.children:
            if isinstance(child, pg.ScatterPlotItem):
                child.show()

    def see_grids(self):
        for child in self.graphqt.children:
            if isinstance(child, CustomGrid):
                child.show()

    def hide_grids(self):
        for child in self.graphqt.children:
            if isinstance(child, CustomGrid):
                child.hide()

    def hide_scatter(self):
        for child in self.graphqt.children:
            if isinstance(child, pg.ScatterPlotItem):
                child.hide()