import sys
import os

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from projectinfo import Ui_WidgetGrid

from loading.loading import load_dataframe, save_df_to_excel, convert_to_dtype


class LoadCPTWidget(QWidget):
    def __init__(self, mainwindow_ref):
        super().__init__()
        # self.vlayout = QVBoxLayout()

        self.main = mainwindow_ref

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.upload_file_btn = QPushButton("Upload File")
        self.upload_file_btn.clicked.connect(self.upload_file)

        self.upload_folder_btn = QPushButton("Upload Folder")
        self.upload_folder_btn.clicked.connect(self.upload_folder)

        self.list_view = QListView()
        self.model = QStandardItemModel(self.list_view)
        self.list_view.setModel(self.model)
        self.list_view.setDragEnabled(True)
        self.list_view.setAcceptDrops(True)
        self.list_view.setDragEnabled(True)

        self.layout.addWidget(self.upload_file_btn)
        self.layout.addWidget(self.upload_folder_btn)
        self.layout.addWidget(self.list_view)

        # self.setCentralWidget(self.tab_widget)

        self.load_cpts_btn = QPushButton("Load CPts")
        self.load_cpts_btn.clicked.connect(self.load_cpts)
        self.layout.addWidget(self.load_cpts_btn)


    def upload_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open file', '', "CSV (*.csv)")
        if file_name:
            print(file_name)
            item = QStandardItem(file_name)
            self.model.appendRow(item)
            # self.df = load_dataframe(file_name)
            print('Item added: ', item.text())
            print(self.model.rowCount())
        else:
            return
        # self.tab2.tableWidget.loadFile(fileName = item.text())

    def upload_folder(self):
        folder_name = QFileDialog.getExistingDirectory(self, 'Open Folder')
        if folder_name:
            self.ffps = []
            for file_name in os.listdir(folder_name):
                if file_name.endswith('.csv'):
                    self.ffps.append(os.path.join(folder_name, file_name))
                    item = QStandardItem(os.path.join(folder_name, file_name))
                    self.model.appendRow(item)
            self.main.df = load_dataframe(self.ffps)
        else:
            return

    def load_cpts(self):

        ffps = [self.model.item(i).text() for i in range(self.model.rowCount())]
        self.main.df = load_dataframe(ffps)
        self.main.tab2.tableWidget.loadDF(path='TEST', df=self.main.df)


class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()

        self.setWindowTitle("Cptspy")
        self.setGeometry(100, 100, 600, 400)
        self.resize(1024, 784)

        self.tab_widget = QTabWidget()

        self.tab0 = QWidget()
        self.tab1 = LoadCPTWidget(self)
        # self.tab2 = ProjReqTab()
        # self.tab2 = Ui_Widget()
        self.tab2 = Ui_WidgetGrid()
        self.tab3 = QWidget()
        # print(type(self.tab2))


        self.df = None
        self.proj_requirements = {}
        self.tab_widget.addTab(self.tab0, "Home")
        self.tab_widget.addTab(self.tab1, "Load CPTs")
        self.tab_widget.addTab(self.tab2, 'Dataframe')
        self.tab_widget.addTab(self.tab3, "Project Info")

        # self.df = None
        # self.tab2_layout = QGridLayout()
        # self.tab2.setLayout(self.tab2_layout)

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
