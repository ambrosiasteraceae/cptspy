from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from load.loading import load_dataframe
import os
from miscellaneous.timed import timed


# @TODO Add refresh button
# @TODO If you start a new proejct it will throw error if nothing is computed. Due to reading output.csv files
# @TODO What happens if you delete the summary files? Should we check for that as well?
# @Todo If you upload folder more than once it doubles the items. We can implement a set
# @TODO When you create a new project and you haven't calculated anyhting, and you exit. The progress is there but theres no DF to read so will throw an erorr
# @TODO Remove loadcsv widget. We should look to add it in another tab.

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
        self.fsets = set()

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
            # print('Item added: ', item.text())
            print(self.model.rowCount())
        else:
            return
        # self.proj_req.tableWidget.loadFile(fileName = item.text())

    def upload_folder_new_proj(self):
        # folder_name = QFileDialog.getExistingDirectory(self, 'Open Folder')
        # folder_name = 'D:/04_R&D/cptspy/output'

        # Lists all files in the self.main.ffp.converted folder
        folder_lists = os.listdir(self.main.ffp.converted)
        self.process_files(folder_lists)

    def process_files(self, folder_lists):

        folder_name = self.main.ffp.converted
        self.ffps = []

        for file_name in folder_lists:
            if file_name.endswith('.csv'):
                self.ffps.append(os.path.join(folder_name, file_name))
                item = QStandardItem(os.path.join(folder_name, file_name))
                # This is to prevent from duplicating elements when pressing the button

                if file_name not in self.fsets:
                    self.model.appendRow(item)
                    self.fsets.add(file_name)

        self.main.thdf = load_dataframe(self.ffps)
        # print('Here is df',self.main.thdf.head())

    # @timed
    def upload_folder_load_proj(self):

        # @TODO self.processed should be self.main.processed
        # @TODO I think that when we calculate and merge pdfs, the list widget will still show since the main.hdf still hold a reference to the first excel, and not the overwritten excel

        self.processed = set(self.main.hdf['ffp'])

        # Maybe this is slow

        all_files = set(self.main.ffp.converted + file_name for file_name in os.listdir(self.main.ffp.converted))
        folder_lists = all_files - self.processed

        self.process_files(folder_lists)
        # print(self.main.thdf)

    def upload_folder(self):
        if self.main.state == 0:
            print('[Load]-Returning new proj func')
            return self.upload_folder_new_proj()
        else:
            # print('csv-returning-old')
            print('[Load]-Returning old proj func')
            return self.upload_folder_load_proj()

    def load_cpts(self):

        ffps = [self.model.item(i).text() for i in range(self.model.rowCount())]

        # if not ffps:
        #     QMessageBox.warning(self, "No Files", "Please upload CSV files before loading CPTs.")
        #     return

        self.main.thdf = load_dataframe(ffps)

        # print('Succesfully loaded {} files'.format(len(ffps)))

        # print(f"CPTs are:{[ffp.split('//')[-1] for ffp in ffps]}")
        self.main.proj_req.tableWidget.loadDF(path='TEST', df=self.main.thdf)
        # print('State of Project', self.main.state)

        # Save the header file if the project is new

        if not os.path.exists(self.main.ffp.summary + 'Header.xlsx'):
            self.main.thdf.to_excel(self.main.ffp.summary + 'Header.xlsx', index=False)
