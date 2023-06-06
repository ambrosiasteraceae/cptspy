from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import QRect, QCoreApplication, QMetaObject, QAbstractTableModel, Qt
import os
import glob
from home import TreeView
from read.reading import *
import shutil
#@TODO IN ANY LOADING CONFIG THERE IS NO RECURSIVE SEARCH?
#@Todo. What if the upload folder just copies the raw files in the raw folder and the uploaded file list view just lists the csv files in the directory
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

        self.layoutleft.addWidget(self.raw_list_widget_title)

        self.list_view_convert = QListView(self.horizontalLayoutWidget)
        self.list_view_convert.setObjectName(u"list_view_convert")
        self.layoutleft.addWidget(self.list_view_convert)
        self.model_convert = QStandardItemModel(self.list_view_convert)
        self.list_view_convert.setModel(self.model_convert)

        self.csets = set()

        self.loaded_files_label = QLabel(self.horizontalLayoutWidget)
        self.loaded_files_label.setObjectName(u"loaded_files_label")

        self.layoutleft.addWidget(self.loaded_files_label)

        self.progressBar = QProgressBar(self.horizontalLayoutWidget)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(24)

        self.layoutleft.addWidget(self.progressBar)

        self.convert = QCommandLinkButton(self.horizontalLayoutWidget)
        self.convert.setObjectName(u"convert")
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

    def upload_folder_btn(self):
        folder_name = QFileDialog.getExistingDirectory(self, 'Open Folder', directory='D:/01_Projects/38.Al Hudayriyat')
        self.ffp = folder_name

        files = glob.glob(self.ffp + '/*.xlsx')
        self.move_files_to_directory(files)
        self.update_list_view()
        print(self.ffp)

    def move_files_to_directory(self, file_list):
        for f in file_list:
            shutil.copy(f, self.main.ffp.raw)

    def update_list_view(self):
        #The idea is to list the files that are yet to be converted. Sitting outside the fail/pass fodlers
        files = glob.glob(self.main.ffp.raw + "*.xlsx")
        for file in files:
            file_name = os.path.basename(file)
            # if file_name not in self.csets:
            item = QStandardItem(file_name)
            self.model_convert.appendRow(item)
                # self.csets.add(file_name)
        self.loaded_files_label.setText(f"{len(files)} raw files loaded")



    def convert_files(self):
        fail = []
        passed = []
        pass

    def update_log(self):
        pass

    def convert_file_gui(self, ffp, out_fp, verbose=0):
        fns = [convert_nmdc_to_csv_00, convert_nmdc_to_csv_01, convert_cs_to_csv_01, convert_cs_to_csv_02]
        for i, fn in enumerate(fns):
            res = fn(ffp, out_fp, verbose=verbose)
            if res == 1:
                return fn.__name__
                passed.append(ffp)
                self.model_log.appendRow(f"{ffp} loaded succesfully")
            else:
                passed.append(fail)
                self.model_log.appendRow(f"{ffp} failed to load.")
            if i == len(fns) - 1:
                self.model_log.appendRow('Reached the end')

    def move_files(self, fail_list, passed_list):
        passed_path = self.ffp + '/pass'
        passed_fail = self.ffp + '/fail'
        if not os.path.exists(passed_path):
            os.makedirs()

# import sys
# app = QApplication(sys.argv)
#
# # Create the widget window
#
# widget = ConvertQT(123)
#
# # Show the widget window
# widget.show()
#
# # Start the event loop
# sys.exit(app.exec())
#
