from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from load.loading import load_dataframe
import os
from miscellaneous.timed import timed
#@TODO Add refresh button
#@TODO If you start a new proejct it will throw error if nothing is computed. Due to reading output.csv files
#@TODO What happens if you delete the summary files? Should we check for that as well?
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

    def upload_folder_new(self):
        # folder_name = QFileDialog.getExistingDirectory(self, 'Open Folder')
        # folder_name = 'D:/04_R&D/cptspy/output'

        #Lists all files in the self.main.ffp.converted folder
        folder_lists = os.listdir(self.main.ffp.converted)
        self.process_files(folder_lists)


    def process_files(self,folder_lists):
        folder_name = self.main.ffp.converted
        self.ffps = []
        for file_name in folder_lists:
            if file_name.endswith('.csv'):
                self.ffps.append(os.path.join(folder_name, file_name))
                item = QStandardItem(os.path.join(folder_name, file_name))
                self.model.appendRow(item)
        self.main.thdf = load_dataframe(self.ffps)
        print('Here is df',self.main.thdf.head())

    # @timed
    def upload_folder_old(self):

        #@TODO self.processed should be self.main.processed
        #@TODO I think that when we calculate and merge pdfs, the list widget will still show since the main.hdf still hold a reference to the first excel, and not the overwritten excel


        self.processed = set(self.main.hdf['ffp'])
        #Maybe this is slow
        all_files = set(self.main.ffp.converted + file_name for file_name in os.listdir(self.main.ffp.converted))
        folder_lists = all_files - self.processed

        self.process_files(folder_lists)
        # print(self.main.thdf)



    def upload_folder(self):
        if self.main.state == 0:
            print('csv-returning-new')
            return self.upload_folder_new()
        else:
            print('csv-returning-old')
            return self.upload_folder_old()



    def load_cpts(self):

        ffps = [self.model.item(i).text() for i in range(self.model.rowCount())]

        self.main.thdf = load_dataframe(ffps)

        print('Succesfully loaded {} files'.format(len(ffps)))

        print(f"CPTs are:{[ffp.split('//')[-1] for ffp in ffps]}")
        self.main.proj_req.tableWidget.loadDF(path='TEST', df=self.main.thdf)
        print('State of Project', self.main.state)

        #Save the header file if the project is new
        if self.main.state == 0:
            self.main.thdf.to_excel(self.main.ffp.summary+'Header.xlsx', index = False)
