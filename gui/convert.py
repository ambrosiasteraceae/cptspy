from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import QRect, QCoreApplication, QMetaObject, QAbstractTableModel, Qt
import os
import glob

# 
# from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
#     QMetaObject, QObject, QPoint, QRect,
#     QSize, QTime, QUrl, Qt)
# from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
#     QFont, QFontDatabase, QGradient, QIcon,
#     QImage, QKeySequence, QLinearGradient, QPainter,
#     QPalette, QPixmap, QRadialGradient, QTransWidget)
# from PySide6.QtWidgets import (QApplication, QCommandLinkButton, QHBoxLayout, QHeaderView,
#     QLabel, QLayout, QListView, QListWidget,
#     QListWidgetItem, QProgressBar, QPushButton, QSizePolicy.Policy.Policy,
#     QSpacerItem, QTreeWidget, QTreeWidgetItem, QVBoxLayout,
#     QWidget)

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

        self.layoutleft.addWidget(self.load_folder_xlsx)

        self.raw_list_widget_title = QLabel(self.horizontalLayoutWidget)
        self.raw_list_widget_title.setObjectName(u"raw_list_widget_title")

        self.layoutleft.addWidget(self.raw_list_widget_title)

        self.listWidget = QListWidget(self.horizontalLayoutWidget)
        self.listWidget.setObjectName(u"listWidget")

        self.layoutleft.addWidget(self.listWidget)

        self.loaded_list_widget = QLabel(self.horizontalLayoutWidget)
        self.loaded_list_widget.setObjectName(u"loaded_list_widget")

        self.layoutleft.addWidget(self.loaded_list_widget)

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

        self.listView = QListView(self.horizontalLayoutWidget)
        self.listView.setObjectName(u"listView")

        self.layoutright.addWidget(self.listView)

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

        self.treeWidget = QTreeWidget(self.horizontalLayoutWidget)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.treeWidget.setHeaderItem(__qtreewidgetitem)
        self.treeWidget.setObjectName(u"treeWidget")

        self.layoutright.addWidget(self.treeWidget)

        self.mainlayout.addLayout(self.layoutright)

        self.mainlayout.setStretch(1, 1)
        self.mainlayout.setStretch(2, 8)

        self.retranslateUi(Widget)

        QMetaObject.connectSlotsByName(Widget)

        self.mainlayout.addLayout(self.layoutright)

    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Widget", None))
        self.load_single_xlsx.setText(QCoreApplication.translate("Widget", u"Upload File", None))
        self.load_folder_xlsx.setText(QCoreApplication.translate("Widget", u"Upload Folder", None))
        self.raw_list_widget_title.setText(QCoreApplication.translate("Widget", u"Uploaded files:", None))
        self.loaded_list_widget.setText(QCoreApplication.translate("Widget", u"Loaded FIles ", None))
        self.convert.setText(QCoreApplication.translate("Widget", u"Convert raw files", None))
        self.label_list_widget_right.setText(QCoreApplication.translate("Widget", u"Converted log:", None))
        self.label_converted.setText(QCoreApplication.translate("Widget", u"Converted", None))
        self.label_failed.setText(QCoreApplication.translate("Widget", u"Failed", None))
        self.project_structure_tree.setText(QCoreApplication.translate("Widget", u"Project Structure", None))
        # retranslateUiQMetaObject.connectSlotsByName(Widget)




    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Widget", None))
        self.load_single_xlsx.setText(QCoreApplication.translate("Widget", u"Upload File", None))
        self.load_folder_xlsx.setText(QCoreApplication.translate("Widget", u"Upload Folder", None))
        self.raw_list_widget_title.setText(QCoreApplication.translate("Widget", u"Uploaded files:", None))
        self.loaded_list_widget.setText(QCoreApplication.translate("Widget", u"Loaded FIles ", None))
        self.convert.setText(QCoreApplication.translate("Widget", u"Convert raw files", None))
        self.label_list_widget_right.setText(QCoreApplication.translate("Widget", u"Converted log:", None))
        self.label_converted.setText(QCoreApplication.translate("Widget", u"Converted", None))
        self.label_failed.setText(QCoreApplication.translate("Widget", u"Failed", None))
        self.project_structure_tree.setText(QCoreApplication.translate("Widget", u"Project Structure", None))
    # retranslateUi

#
# import sys
# app = QApplication(sys.argv)
#
# # Create the widget window
#
# widget = ConvertQT()
#
# # Show the widget window
# widget.show()
#
# # Start the event loop
# sys.exit(app.exec())

