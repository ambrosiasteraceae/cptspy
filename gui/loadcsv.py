import os
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from load.loading import load_dataframe
from miscellaneous.timed import timed
from PyQt6.uic import loadUi
import pandas as pd
from extras import GreenMessageBox, RedMessageBox


class LoadQT(QWidget):
    def __init__(self, mainwindow_ref):
        super().__init__()

        self.main = mainwindow_ref
        loadUi('uis/load2.ui', self)

        self.model = QStandardItemModel(self.list_view)
        self.list_view.setModel(self.model)
        self.fsets = set()

        self.upload_folder_btn.clicked.connect(self.upload_folder_load_proj)
        self.upload_everything_btn.clicked.connect(self.upload_folder_new_proj)

        self.previous_btn.clicked.connect(self.main.tab_widget.previous)
        self.next_btn.clicked.connect(self.main.tab_widget.next)

    def upload_folder_load_proj(self):
        """
        Currently:

        1 -> It looks for what was added in the results.xlsx and store in self.processed set
        2 -> We list all files that are in summary folder and store in the set.

        3 -> We look for differences and upload only the unique files
        "checks only in the header, but that doesnt mean that the results are there. better we look for .npz files"
        """


        # self.processed = set(self.main.hdf['ffp']) #SHould be just converted?
        # all_files = set(self.main.ffp.converted + file_name for file_name in os.listdir(self.main.ffp.converted))

        #A better way
        if os.path.exists(self.main.ffp.summary + 'Results.xlsx'):
            self.processed = set(self.main.df['CPT-ID'] + '.csv') #what was processed
        else:
            self.processed = set()

        all_files = set(os.listdir(self.main.ffp.converted))
        difference = all_files - self.processed

        if len(difference) != 0:
            self.process_files([self.main.ffp.converted + fname for fname in difference])
            GreenMessageBox(f'{len(difference)} files have been uploaded.')
        else:
            GreenMessageBox(f'There are no files to upload.')


    def upload_folder_new_proj(self):
        """
         # Lists all files in the self.main.ffp.converted folder

        """
        folder_lists = os.listdir(self.main.ffp.converted)
        self.process_files(folder_lists)

    def process_files(self, folder_lists):

        """
        We essentialy load all the unique files
        """

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
        self.uploaded_files_label.setText(f"Uploaded Files: {len(self.fsets)}")
        if self.main.thdf.empty:
            self.main.thdf = load_dataframe(self.ffps)
        else:
            extra_df = load_dataframe(self.ffps)
            self.main.thdf = pd.concat([self.main.thdf, extra_df], ignore_index=True)
            self.main.thdf.drop_duplicates(subset = ['CPT-ID'], inplace = True)
            extra_df = pd.DataFrame()



    def upload_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open file', '', "CSV (*.csv)")
        if file_name:
            print(file_name)
            item = QStandardItem(file_name)
            self.model.appendRow(item)
            print(self.model.rowCount())
        else:
            return

