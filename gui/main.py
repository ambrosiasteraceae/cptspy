import sys


import pandas as pd
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from projectinfo import ProjReqWidget
from loadcsv import LoadCSVWidget
from runcalc import CalcWidget
from home import HomeQT
from convert import ConvertQT
from overview import OverviewQT
from test import SomethingQT

#@TODO Whenever you load / create and press cancel the program crashes
#@TODO YOU created a new project. You added some files, deleted others. You run and calc for converted files. You exit. You want to open project again, but header.xlsx is not saved.
#TODO: @IDEA Maybe have a single instance of self.file_saved in the main window. It doesn't sotre the file extension but just the basename path. We use this to check if the file is saved.
#TODO when you load a folder not containing folder files, throw warning
class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()

        self.setWindowTitle("Cptspy")
        self.setGeometry(100, 100, 600, 400)
        self.resize(1280, 1024)

        self.tab_widget = QTabWidget()



        self.home = HomeQT(self)
        self.convert = ConvertQT(self)
        self.loadcsv = LoadCSVWidget(self)
        self.proj_req = ProjReqWidget(self)
        self.calc = CalcWidget(self)
        self.overview = OverviewQT(self)

        self.something = SomethingQT(self)



        self.ffp = None #project file path

        #Main dfs
        self.hdf = pd.DataFrame() #project header
        self.df = pd.DataFrame() #project df

        #Temporary
        self.thdf = pd.DataFrame() #temporary header df
        self.tdf = pd.DataFrame() #temporary df

        self.state = 0 #0 = new project, 1 = project loaded
        self.processed = set()

        self.proj_requirements = {}

        self.tab_widget.addTab(self.home, "Home")
        self.tab_widget.addTab(self.convert, "Convert")
        self.tab_widget.addTab(self.loadcsv, "Load")
        self.tab_widget.addTab(self.overview, "Overview")
        self.tab_widget.addTab(self.proj_req, "Requirements")
        self.tab_widget.addTab(self.calc, "Analysis")
        self.tab_widget.addTab(self.something, "Something")

        self.tab_widget.setTabPosition(QTabWidget.TabPosition.West)



        self.setCentralWidget(self.tab_widget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_font = QFont("Source Sans Pro", 9)
    app.setFont(my_font)
    main = MyWindow()
    main.show()
    with open("uis/white_theme.qss", "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)

#add app font

    sys.exit(app.exec())
