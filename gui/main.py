import sys
import pandas as pd


from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from projectinfo import ProjReqWidget
from loadcsv import LoadQT
from runcalc import CalcWidget
from home import HomeQT
from convert import ConvertQT
from overview import OverviewQT
from extras import TabWidgetManager
from graphqt import GraphQT
# from gui.graph.graphqt import GraphQT
# import os
#
# current_dir = os.path.dirname(os.path.abspath(__file__))
# graph_dir = os.path.join(current_dir, 'gui', 'graph')
# sys.path.append(graph_dir)
#TODO Add an excluded folder to converted files to avoid some issus with the converted files
class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()

        self.setWindowTitle("Cptspy")
        self.setGeometry(100, 100, 600, 400)
        self.resize(1400, 1200)

        # self.tab_widget = QTabWidget()

        self.tab_widget = TabWidgetManager()


        # self.tab_manager = TabManager(self.tab_widget)


        self.home = HomeQT(self)
        self.convert = ConvertQT(self)
        self.loadcsv = LoadQT(self)
        self.proj_req = ProjReqWidget(self)
        self.calc = CalcWidget(self)
        self.overview = OverviewQT(self)
        self.graph = GraphQT(self)

        # self.something = SomethingQT(self)
        # self.home2 = HomeQT2(self)

        self.ffp = None #project file path

        #Main dfs
        self.hdf = pd.DataFrame() #project header
        self.df = pd.DataFrame() #project df

        #Temporary
        self.thdf = pd.DataFrame() #temporary header df
        self.tdf = pd.DataFrame() #temporary df

        self.processed = set()
        self.proj_requirements = {}

        self.tab_widget.addTab(self.home, "Home")
        self.tab_widget.addTab(self.proj_req, "Settings")
        self.tab_widget.addTab(self.convert, "Convert")
        self.tab_widget.addTab(self.loadcsv, "Load")
        self.tab_widget.addTab(self.overview, "Overview")
        self.tab_widget.addTab(self.calc, "Analysis")
        self.tab_widget.addTab(self.graph, "Graph")

        # self.tab_widget.addTab(self.something, "Something")
        # self.tab_widget.addTab(self.home2, "Convert2")

        self.tab_widget.setTabPosition(QTabWidget.TabPosition.West)
        self.setCentralWidget(self.tab_widget)

        # print(self.tab_widget.currentChanged.connect(self.tab_event))
        # # self.tab_widget.setCurrentIndex(7)
        # print(self.tab_widget.count())
        # print(self.tab_widget.currentIndex())



    # def tab_event(self):
    #     print(self.tab_widget.currentIndex())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_font = QFont("Source Sans Pro", 9)
    app.setFont(my_font)
    main = MyWindow()
    main.show()
    with open("uis/white_theme.qss", "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)

    sys.exit(app.exec())
