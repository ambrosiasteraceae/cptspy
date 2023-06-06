from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import QRect, QCoreApplication, QMetaObject, QAbstractTableModel, Qt

from projectinfo import PDWidget
from home import HomeQT
import pandas as pd
import os
from home import TreeView

def on_radio_button_clicked(msg):
    message_box = QMessageBox()
    message_box.setWindowTitle("Information")
    message_box.setText(f"{msg}")
    message_box.exec()


class OverviewQT(QWidget):
    def __init__(self, main_window_ref):
        self.main = main_window_ref
        super(OverviewQT, self).__init__()
        self.setupUi(self)

    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(1049, 813)
        self.horizontalLayoutWidget = QWidget(Widget)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(40, 10, 951, 751))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        self.verticalLayout_2.setContentsMargins(-1, -1, 0, -1)
        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)

        self.label = QLabel(self.horizontalLayoutWidget)
        self.label.setObjectName(u"label")

        self.verticalLayout_2.addWidget(self.label)

        self.line_2 = QFrame(self.horizontalLayoutWidget)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.line_2.setFrameShadow(QFrame.Shadow.Raised)

        self.line_2.setLineWidth(1)
        self.line_2.setMidLineWidth(2)
        self.line_2.setFrameShape(QFrame.Shape.HLine)

        self.verticalLayout_2.addWidget(self.line_2)

        self.radioButton_1 = QRadioButton(self.horizontalLayoutWidget)
        self.radioButton_1.setObjectName(u"radioButton_1")
        self.radioButton_1.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        self.verticalLayout_2.addWidget(self.radioButton_1)

        self.radioButton_2 = QRadioButton(self.horizontalLayoutWidget)
        self.radioButton_2.setObjectName(u"radioButton_2")
        self.radioButton_2.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        self.verticalLayout_2.addWidget(self.radioButton_2)

        self.merge_dfs = QPushButton(self.horizontalLayoutWidget)
        self.merge_dfs.setObjectName(u"merge_dfs")
        self.merge_dfs.clicked.connect(self.merge_dataframes)
        self.merge_dfs.setEnabled(True)


        self.verticalLayout_2.addWidget(self.merge_dfs)

        self.label_2 = QLabel(self.horizontalLayoutWidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.label_2.setAutoFillBackground(False)

        self.verticalLayout_2.addWidget(self.label_2)

        self.line = QFrame(self.horizontalLayoutWidget)
        self.line.setObjectName(u"line")
        self.line.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.line.setFrameShadow(QFrame.Shadow.Raised)
        self.line.setLineWidth(1)
        self.line.setMidLineWidth(2)
        self.line.setFrameShape(QFrame.Shape.HLine)

        self.verticalLayout_2.addWidget(self.line)

        self.radioButton_3 = QRadioButton(self.horizontalLayoutWidget)
        self.radioButton_3.setObjectName(u"radioButton_3")
        self.radioButton_3.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        self.verticalLayout_2.addWidget(self.radioButton_3)

        self.radioButton_4 = QRadioButton(self.horizontalLayoutWidget)
        self.radioButton_4.setObjectName(u"radioButton_4")
        self.radioButton_4.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        self.verticalLayout_2.addWidget(self.radioButton_4)

        self.verticalSpacer = QSpacerItem(20, 75, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_4 = QLabel(self.horizontalLayoutWidget)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_3.addWidget(self.label_4)





        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.tree = TreeView()
        # self.tree = QTreeWidget(self.horizontalLayoutWidget)
        # __qtreewidgetitem = QTreeWidgetItem()
        # __qtreewidgetitem.setText(0, u"1");
        # self.tree.setHeaderItem(__qtreewidgetitem)
        # self.tree.setObjectName(u"tree")


        self.toolButton = QToolButton(self.horizontalLayoutWidget)
        self.toolButton.clicked.connect(self.tree.refresh)
        self.toolButton.setObjectName(u"toolButton")
        icon = QIcon(QIcon.fromTheme(u"sync-synchronizing"))
        self.toolButton.setIcon(icon)
        self.horizontalLayout_3.addWidget(self.toolButton)


        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tree.sizePolicy().hasHeightForWidth())
        self.tree.setSizePolicy(sizePolicy)

        self.verticalLayout_2.addWidget(self.tree)

        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_3 = QLabel(self.horizontalLayoutWidget)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout.addWidget(self.label_3)

        # self.table = QTableWidget(self.horizontalLayoutWidget)
        self.table = PDWidget()
        self.table.setObjectName(u"table")

        self.verticalLayout.addWidget(self.table)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_7 = QLabel(self.horizontalLayoutWidget)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout_2.addWidget(self.label_7)

        self.label_6 = QLabel(self.horizontalLayoutWidget)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_2.addWidget(self.label_6)

        self.label_5 = QLabel(self.horizontalLayoutWidget)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_2.addWidget(self.label_5)

        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout.addLayout(self.verticalLayout)

        self.setLayout(self.horizontalLayout)

        self.retranslateUi(Widget)

        QMetaObject.connectSlotsByName(Widget)

        self.radioButton_1.clicked.connect(self.view_temp_header)
        self.radioButton_2.clicked.connect(self.view_temp_results)
        self.radioButton_3.clicked.connect(self.view_main_header)
        self.radioButton_4.clicked.connect(self.view_main_results)



    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Form", None))
        self.label.setText(QCoreApplication.translate("Widget", u"Newly Added", None))
        self.radioButton_1.setText(QCoreApplication.translate("Widget", u"Header", None))
        self.radioButton_2.setText(QCoreApplication.translate("Widget", u"TempResults", None))
        self.merge_dfs.setText(QCoreApplication.translate("Widget", u"Merge with current DF", None))
        self.label_2.setText(QCoreApplication.translate("Widget", u"Project", None))
        self.radioButton_3.setText(QCoreApplication.translate("Widget", u"Header", None))
        self.radioButton_4.setText(QCoreApplication.translate("Widget", u"Results", None))
        self.label_4.setText(QCoreApplication.translate("Widget", u"Project Structure", None))
        self.toolButton.setText("Refresh")
        self.label_3.setText(QCoreApplication.translate("Widget", u"Summary", None))
        self.label_7.setText(QCoreApplication.translate("Widget", u"label_no_files", None))
        self.label_6.setText(QCoreApplication.translate("Widget", u"TextLabel", None))
        self.label_5.setText(QCoreApplication.translate("Widget", u"TextLabel", None))

    # retranslateUi

    def view_main_header(self):
        if not self.main.hdf.empty:
            self.table.loadDF('123', self.main.hdf)
            return
        on_radio_button_clicked('No Project Header was Added nor Created')
        # self.radioButton_3.setChecked(False)
        # self.get_current_radio_check()
    def view_main_results(self):
        if not self.main.df.empty:
            self.table.loadDF('123', self.main.df)
            return
        on_radio_button_clicked('No Project Calc was Added nor Created')
        # self.radioButton_4.setChecked(False)
        # self.get_current_radio_check()

    def view_temp_header(self):
        if not self.main.thdf.empty:
            self.table.loadDF('123', self.main.thdf)
            return
        on_radio_button_clicked('No Newly files were Added nor Created')
        self.table.loadDF('123', self.main.thdf)
        # self.radioButton_1.setChecked(False)
        # self.get_current_radio_check()

    def view_temp_results(self):
        if not self.main.tdf.empty:
            self.table.loadDF('123', self.main.tdf)
            return
        on_radio_button_clicked('No Newly files were Added nor Created - Calc')
        # self.radioButton_2.setChecked(False)
        # self.get_current_radio_check()

    def get_current_radio_check(self):
        radios = self.findChildren(QRadioButton)
        for radio in radios:
            if radio.isChecked():
                return radio.setChecked(True)

    def merge_dataframes(self):

        #Can be applied multiple times - ERROR
        if self.main.state == 1:
            if self.main.tdf.empty or self.main.thdf.empty:
                on_radio_button_clicked(f"{'No new files have been loaded' if self.main.thdf.empty else 'Results have not been computed'}")
                return

            self.main.df = pd.concat([self.main.df, self.main.tdf], ignore_index=True)
            self.main.hdf = pd.concat([self.main.hdf, self.main.thdf], ignore_index=True)

            #save to excel
            self.main.df.to_excel(self.main.ffp.summary + 'Results.xlsx', index=False)
            self.main.hdf.to_excel(self.main.ffp.summary + 'Header.xlsx', index=False)
            self.merge_dfs.setEnabled(False)

        print('Newly Added CPTS has been succesfully merged with the current tables')
        return

# import sys
#
# app = QApplication(sys.argv)
#
# window = OverviewQT('123')
# window.show()
#
# app.exec()
#
# sys.exit(0)
