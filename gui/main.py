import sys
import os

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from projectinfo import ProjReqWidget
from loadcsv import LoadCSVWidget
from runcalc import CalcWidget
from home import HomeQT
from convert import ConvertQT

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
        # self.proj_req = ProjReqTab()
        # self.proj_req = Ui_Widget()
        self.proj_req = ProjReqWidget(self)
        self.calc = CalcWidget(self)
        # print(type(self.proj_req))

        self.ffp = None #project file path
        self.df = None
        self.proj_requirements = {}
        self.tab_widget.addTab(self.home, "Home")
        self.tab_widget.addTab(self.convert, "Convert")
        self.tab_widget.addTab(self.loadcsv, "Load")
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

    sys.exit(app.exec())
