from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from load.loading import load_dataframe
import os

class LoadCSVWidget(QWidget):
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
        # self.proj_req.tableWidget.loadFile(fileName = item.text())

    def upload_folder(self):
        # folder_name = QFileDialog.getExistingDirectory(self, 'Open Folder')
        # folder_name = 'D:/04_R&D/cptspy/output'

        print(self.main.ffp.converted)
        folder_name = self.main.ffp.converted
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
        print('Succesfully loaded {} files'.format(len(ffps)))
        self.main.proj_req.tableWidget.loadDF(path='TEST', df=self.main.df)
        self.main.df.to_excel(self.main.ffp.summary+'Header.xlsx')
