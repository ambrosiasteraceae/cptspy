import pandas as pd
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import QRect, QCoreApplication, QMetaObject, QAbstractTableModel, Qt
import os
import glob
from home import TreeView
from read.reading import *
import shutil


def escape(string):
    extensions = ['PO', 'PRE']
    for ext in extensions:
        if ext in string:
            return ext + string.split(ext)[1].split('.')[0]
    return string.split('.')[0]

#@TODO Tree structure doesnt hsow fail or pass (recursive level 1)
#@TODO IN ANY LOADING CONFIG THERE IS NO RECURSIVE SEARCH? if yuou have nested folders with cpts
#@Todo. What if the upload folder just copies the raw files in the raw folder and the uploaded file list view just lists the csv files in the directory
#@TODO ERROR: YOU CAN STILL LOAD A FODLER THAT HAS THE SAME FILES AS THE ONES IN THE FAIL OR PASS FOLDER
#@TODO.One unique file in the folder you want to uploaded and it will place the whole folder! (fixed)
#@TODO IF you upload more than  one folder in the same session, the left list view widget will get overwritten. But we want to append!

class ConvertQT(QWidget):
    def __init__(self, main_window_ref):
        super(ConvertQT, self).__init__()
        self.main = main_window_ref
        self.setupUi(self)

    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(1122, 827)
        Widget.setWindowOpacity(0.000000000000000)
        Widget.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        Widget.setAutoFillBackground(False)
        self.horizontalLayoutWidget = QWidget(Widget)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(0, 0, 651, 651))
        self.mainlayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.mainlayout.setSpacing(15)
        self.mainlayout.setObjectName(u"mainlayout")
        self.mainlayout.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)
        self.mainlayout.setContentsMargins(20, 9, 0, 0)
        self.layoutleft = QVBoxLayout()
        self.layoutleft.setObjectName(u"layoutleft")
        self.load_single_xlsx = QPushButton(self.horizontalLayoutWidget)
        self.load_single_xlsx.setObjectName(u"load_single_xlsx")

        self.layoutleft.addWidget(self.load_single_xlsx)

        self.load_folder_xlsx = QPushButton(self.horizontalLayoutWidget)
        self.load_folder_xlsx.setObjectName(u"load_folder_xlsx")
        self.load_folder_xlsx.clicked.connect(self.upload_folder_btn)

        self.layoutleft.addWidget(self.load_folder_xlsx)

        self.raw_list_widget_title = QLabel(self.horizontalLayoutWidget)
        self.raw_list_widget_title.setObjectName(u"raw_list_widget_title")

        # LIST VIEW LEFT
        self.list_view_convert = QListView(self.horizontalLayoutWidget)
        self.list_view_convert.setObjectName(u"list_view_convert")
        self.layoutleft.addWidget(self.list_view_convert)
        self.model_convert = QStandardItemModel(self.list_view_convert)
        self.list_view_convert.setModel(self.model_convert)

        self.layoutleft.addWidget(self.raw_list_widget_title)

        self.csets = set()

        self.loaded_files_label = QLabel(self.horizontalLayoutWidget)
        self.loaded_files_label.setObjectName(u"loaded_files_label")

        self.layoutleft.addWidget(self.loaded_files_label)

        self.progressBar = QProgressBar(self.horizontalLayoutWidget)
        self.progressBar.setObjectName(u"progressBar")
        # self.progressBar.setValue(0)

        self.layoutleft.addWidget(self.progressBar)

        self.convert = QCommandLinkButton(self.horizontalLayoutWidget)
        self.convert.setObjectName(u"convert")
        self.convert.clicked.connect(self.convert_files)
        # self.convert.setCursor(QCursor(Qt.ArrowCursor))
        # self.convert.setCheckable(False)


        self.layoutleft.addWidget(self.convert)

        self.mainlayout.addLayout(self.layoutleft)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.mainlayout.addItem(self.horizontalSpacer)

        self.layoutright = QVBoxLayout()
        self.layoutright.setObjectName(u"layoutright")
        self.label_list_widget_right = QLabel(self.horizontalLayoutWidget)
        self.label_list_widget_right.setObjectName(u"label_list_widget_right")

        self.layoutright.addWidget(self.label_list_widget_right)

        ### LIST VIEWS ###
        # LIST VIEW RIGHT
        self.list_view_log = QListView(self.horizontalLayoutWidget)
        self.list_view_log.setObjectName(u"list_view_log")
        self.model_log = QStandardItemModel(self.list_view_log)
        self.list_view_log.setModel(self.model_log)

        self.layoutright.addWidget(self.list_view_log)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(-1, 12, -1, -1)
        self.label_converted = QLabel(self.horizontalLayoutWidget)
        self.label_converted.setObjectName(u"label_converted")

        self.horizontalLayout_2.addWidget(self.label_converted)

        self.label_failed = QLabel(self.horizontalLayoutWidget)
        self.label_failed.setObjectName(u"label_failed")

        self.horizontalLayout_2.addWidget(self.label_failed)

        self.layoutright.addLayout(self.horizontalLayout_2)

        self.verticalSpacer = QSpacerItem(20, 15, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.layoutright.addItem(self.verticalSpacer)

        self.project_structure_tree = QLabel(self.horizontalLayoutWidget)
        self.project_structure_tree.setObjectName(u"project_structure_tree")

        self.layoutright.addWidget(self.project_structure_tree)

        self.treeview = TreeView()
        self.treeview.setObjectName(u"treeview")

        self.layoutright.addWidget(self.treeview)

        self.mainlayout.addLayout(self.layoutright)

        self.mainlayout.setStretch(1, 1)
        self.mainlayout.setStretch(2, 8)

        self.retranslateUi(Widget)

        QMetaObject.connectSlotsByName(Widget)

        self.mainlayout.addLayout(self.layoutright)

        self.uploaded_files = set()



    def get_all_pass_and_fail_files(self):
        dirs = ['pass/', 'fail/']
        processed = set()

        for directory in dirs:
            ffp = os.path.join(self.main.ffp.raw, directory)


            if not os.path.exists(ffp):
                return processed

            _files = glob.glob(ffp + '*.xlsx')
            _files = [os.path.basename(f) for f in _files]
            processed.update(set(_files))

        return processed


    def upload_file(self):
        pass

    def upload_folder_btn(self):

        folder_name = QFileDialog.getExistingDirectory(self, 'Open Folder', directory='D:/01_Projects/38.Al Hudayriyat')
        folder_files = glob.glob(folder_name + '/*.xlsx')

        self.processed = self.get_all_pass_and_fail_files()
        _files_to_copy = [os.path.basename(f) for f in folder_files]

        _files_to_copy = set(_files_to_copy) - self.processed #files_to_copy now only holds the path_basename


        files_to_copy = [os.path.join(folder_name, f) for f in _files_to_copy]


        if files_to_copy:
            self.progressBar.setValue(0)
            self.move_files_to_directory(files_to_copy)
            self.update_list_view()
        elif not folder_files:
            QMessageBox.warning(self, 'Warning', 'No .xlsx files in the folder')
        else:
            QMessageBox.warning(self, 'Warning', 'You are trying to insert files that have already been uploaded')


    def move_files_to_directory(self, file_list):
        for f in file_list:
            shutil.copy(f, self.main.ffp.raw)

    def update_list_view(self):
        # The idea is to list the files that are yet to be converted. Sitting outside the fail/pass fodlers
        files_to_add = glob.glob(self.main.ffp.raw + "*.xlsx")
        if files_to_add:
            print(f"{len(files_to_add)} being updated")
            new_files = set(files_to_add) - self.uploaded_files

            if new_files:
                self.uploaded_files.update(new_files)
                for file_name in new_files:
                    self.model_convert.appendRow(QStandardItem(os.path.basename(file_name)))
        self.loaded_files_label.setText(f"{len(files_to_add)} raw files loaded")
        self.treeview.refresh()


    def convert_files(self):

        passed_path = os.path.join(self.main.ffp.raw, 'pass/')
        failed_path = os.path.join(self.main.ffp.raw, 'fail/')

        self.pass_nr = 0
        self.fail_nr = 0

        if not os.path.exists(passed_path):
            os.makedirs(passed_path)
        if not os.path.exists(failed_path):
            os.makedirs(failed_path)

        for i, file in enumerate(self.uploaded_files):
            self.convert_file_gui(file, passed_path, failed_path)

            percentage = int(i/len(self.uploaded_files)* 100)
            if percentage % 5 == 0:
                self.progressBar.setValue(percentage)


        self.uploaded_files = set()
        self.progressBar.setValue(100)

        self.update_list_view()
        self.model_convert.clear()

        self.label_converted.setText(f"Converted: {self.pass_nr} files")
        self.label_failed.setText(f"Failed: {self.fail_nr} files")



    def convert_file_gui(self, ffp, ffp_passed, ffp_fail):

        fns = [convert_nmdc_to_csv_00, convert_nmdc_to_csv_01, convert_cs_to_csv_01, convert_cs_to_csv_02]
        for i, fn in enumerate(fns):
            res = fn(ffp)
            file_name = os.path.basename(ffp)
            file_name_shortcut = escape(file_name)
            if isinstance(res, pd.DataFrame):
                # We found the right converter
                res.to_csv(self.main.ffp.converted + f"{file_name.split('.')[0]}.csv", index=False, sep=';')
                os.rename(ffp, os.path.join(ffp_passed, file_name))
                self.model_log.appendRow(QStandardItem(f"{file_name_shortcut} loaded successfully."))
                self.pass_nr +=1
                return

            if i == len(fns) - 1:
                # We reached the end of the list and no converter was found
                os.rename(ffp, os.path.join(ffp_fail, file_name))
                self.model_log.appendRow(QStandardItem(f"{file_name_shortcut} failed to load."))
                self.fail_nr +=1


    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Widget", None))
        self.load_single_xlsx.setText(QCoreApplication.translate("Widget", u"Upload File", None))
        self.load_folder_xlsx.setText(QCoreApplication.translate("Widget", u"Upload Folder", None))
        self.raw_list_widget_title.setText(QCoreApplication.translate("Widget", u"Uploaded files:", None))
        self.loaded_files_label.setText(QCoreApplication.translate("Widget", u"Loaded FIles ", None))
        self.convert.setText(QCoreApplication.translate("Widget", u"Convert raw files", None))
        self.label_list_widget_right.setText(QCoreApplication.translate("Widget", u"Converted log:", None))
        self.label_converted.setText(QCoreApplication.translate("Widget", u"Converted", None))
        self.label_failed.setText(QCoreApplication.translate("Widget", u"Failed", None))
        self.project_structure_tree.setText(QCoreApplication.translate("Widget", u"Project Structure", None))
        # retranslateUiQMetaObject.connectSlotsByName(Widget)

