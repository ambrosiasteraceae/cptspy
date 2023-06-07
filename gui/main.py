import sys
import os

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


#@TODO Whenever you load / create and press cancel the program crashes
#@TODO YOU created a new project. You added some files, deleted others. You run and calc for converted files. You exit. You want to open project again, but header.xlsx is not saved.
#TODO: @IDEA Maybe have a single instance of self.file_saved in the main window. It doesn't sotre the file extension but just the basename path. We use this to check if the file is saved.

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
        self.tab_widget.addTab(self.proj_req, "Project Info")
        self.tab_widget.addTab(self.calc, "Run Calculations")

        # self.df = None
        # self.tab2_layout = QGridLayout()
        # self.proj_req.setLayout(self.tab2_layout)

        # self.upload_file_btn = QPushButton("Upload File")
        # self.upload_file_btn.clicked.connect(self.upload_file)
        #
        # self.upload_folder_btn = QPushButton("Upload Folder")
        # self.upload_folder_btn.clicked.connect(self.upload_folder)
        #
        # self.list_view = QListView()
        # self.model = QStandardItemModel(self.list_view)
        # self.list_view.setModel(self.model)
        # self.list_view.setDragEnabled(True)
        # self.list_view.setAcceptDrops(True)
        # self.list_view.setDragEnabled(True)
        #
        # self.tab1_layout.addWidget(self.upload_file_btn)
        # self.tab1_layout.addWidget(self.upload_folder_btn)
        # self.tab1_layout.addWidget(self.list_view)

        self.setCentralWidget(self.tab_widget)

        # self.load_cpts_btn = QPushButton("Load CPts")
        # self.load_cpts_btn.clicked.connect(self.load_cpts)
        # self.tab1_layout.addWidget(self.load_cpts_btn)









if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = MyWindow()
    main.show()
    with open("style.qss", "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)

    sys.exit(app.exec())
