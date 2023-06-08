import os

from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QDoubleValidator, QIntValidator, QValidator
import sys
import pandas as pd
import json
from PyQt6.QtGui import *
#TODO Lood btn throws error when trying to load a file that doesnt exist

def parse_proj_requirements(line_edits):
    proj_req = {}
    for lineEdit in line_edits:
        try:
            val = int(lineEdit.text())
        except ValueError:
            try:
                val = float(lineEdit.text())
            except ValueError:
                val = lineEdit.text()

        proj_req[lineEdit.objectName()] = val
    return proj_req

class PandasModel(QAbstractTableModel):
    def __init__(self, df = pd.DataFrame(), parent=None):
        QAbstractTableModel.__init__(self, parent=parent)
        self._df = df

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role != Qt.ItemDataRole.DisplayRole:
            return QVariant()

        if orientation == Qt.Orientation.Horizontal:
            try:
                return self._df.columns.tolist()[section]
            except (IndexError, ):
                return QVariant()
        elif orientation == Qt.Orientation.Vertical:
            try:
                # return self.df.index.tolist()
                return self._df.index.tolist()[section]
            except (IndexError, ):
                return QVariant()

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role != Qt.ItemDataRole.DisplayRole:
            return QVariant()

        if not index.isValid():
            return QVariant()

        return QVariant(str(self._df.iloc[index.row(), index.column()]))

    def setData(self, index, value, role):
        row = self._df.index[index.row()]
        col = self._df.columns[index.column()]
        if hasattr(value, 'toPyObject'):
            # PyQt4 gets a QVariant
            value = value.toPyObject()
        else:
            # PySide gets an unicode
            dtype = self._df[col].dtype
            if dtype != object:
                value = None if value == '' else dtype.type(value)
        self._df.set_value(row, col, value)
        return True

    def rowCount(self, parent=QModelIndex()):
        return len(self._df.index)

    def columnCount(self, parent=QModelIndex()):
        return len(self._df.columns)

    def sort(self, column, order):
        colname = self._df.columns.tolist()[column]
        self.layoutAboutToBeChanged.emit()
        self._df.sort_values(colname, ascending= order == Qt.SortOrder.AscendingOrder, inplace=True)
        self._df.reset_index(inplace=True, drop=True)
        self.layoutChanged.emit()


class PDWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=None)
        vLayout = QVBoxLayout(self)
        hLayout = QHBoxLayout()
        # self.pathLE = QLineEdit(self)
        # hLayout.addWidget(self.pathLE)
        # self.loadBtn = QPushButton("Select File", self)
        # hLayout.addWidget(self.loadBtn)
        vLayout.addLayout(hLayout)
        self.pandasTv = QTableView(self)
        vLayout.addWidget(self.pandasTv)
        # self.loadBtn.clicked.connect(self.loadFile)
        self.pandasTv.setSortingEnabled(True)


        class CustomDelegate(QStyledItemDelegate):
            def paint(self, painter, option, index):
                # Custom painting code here
                if index.row() % 2 == 0:
                    painter.fillRect(option.rect, QColor(220,220,220))  # Alternate row color 1
                else:
                    painter.fillRect(option.rect, QColor(255,255,255))  # Alternate row color 2

                # Call the base class paint() method to handle other painting tasks
                super().paint(painter, option, index)

        delegate = CustomDelegate(self)
        self.pandasTv.setItemDelegate(delegate)

    def loadFile(self):
        # if fileName is None:
        fileName, _ = QFileDialog.getOpenFileName(self, "Open File", "", "CSV Files (*.csv)");
        # self.pathLE.setText(fileName)
        # if df is None:
        df = pd.read_csv(fileName, delimiter=';')
        model = PandasModel(df)
        self.pandasTv.setModel(model)

    def loadDF(self, path, df):
        # self.pathLE.setText(path)
        model = PandasModel(df)
        self.pandasTv.setModel(model)


class ProjReqWidget(QWidget):
    def __init__(self, main_window_ref,parent=None):
        super(ProjReqWidget, self).__init__(parent)
        self.main = main_window_ref
        self.setupUi(self)

    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(1024, 784)
        self.widget = QWidget(Widget)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(20, 80, 991, 612))
        self.gridLayout = QGridLayout(self.widget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)


        self.lineEdit_10 = QLineEdit(self.widget)
        self.lineEdit_10.setObjectName(u"m_w")
        self.lineEdit_10.setPlaceholderText(u"Insert Magnitude of Earthquake")
        #allow certain input
        onlyFloat = QDoubleValidator()
        self.lineEdit_10.setValidator(onlyFloat)


        self.gridLayout.addWidget(self.lineEdit_10, 0, 0, 1, 2)

        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 2, 1, 1)

        self.tableWidget = PDWidget(self.widget)
        self.tableWidget.setObjectName(u"tableWidget")

        self.gridLayout.addWidget(self.tableWidget, 0, 3, 22, 1)

        self.lineEdit_11 = QLineEdit(self.widget)
        self.lineEdit_11.setObjectName(u"pga")
        self.lineEdit_11.setPlaceholderText(u"Insert Peak Ground Acceleration in g(m/s2)")
        self.lineEdit_11.setValidator(onlyFloat)

        self.gridLayout.addWidget(self.lineEdit_11, 1, 0, 1, 2)

        self.label_2 = QLabel(self.widget)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 1, 2, 1, 1)

        self.lineEdit_12 = QLineEdit(self.widget)
        self.lineEdit_12.setObjectName(u"gwl")
        self.lineEdit_12.setPlaceholderText(u"Insert Ground Water Level in m")

        self.gridLayout.addWidget(self.lineEdit_12, 2, 0, 1, 2)

        self.label_3 = QLabel(self.widget)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 2, 2, 1, 1)

        self.lineEdit_13 = QLineEdit(self.widget)
        self.lineEdit_13.setObjectName(u"scf")
        self.lineEdit_13.setPlaceholderText(u"Insert Shell Correction Factor")

        self.gridLayout.addWidget(self.lineEdit_13, 3, 0, 1, 2)

        self.label_4 = QLabel(self.widget)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 3, 2, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 18, QSizePolicy.Policy.Minimum,  QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 4, 1, 1, 1)

        self.lineEdit = QLineEdit(self.widget)
        self.lineEdit.setObjectName(u"proj_name")

        self.gridLayout.addWidget(self.lineEdit, 5, 0, 1, 2)

        self.label_5 = QLabel(self.widget)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 5, 2, 1, 1)

        self.lineEdit_2 = QLineEdit(self.widget)
        self.lineEdit_2.setObjectName(u"proj_num")


        self.gridLayout.addWidget(self.lineEdit_2, 6, 0, 1, 2)

        self.label_6 = QLabel(self.widget)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 6, 2, 1, 1)

        self.lineEdit_3 = QLineEdit(self.widget)
        self.lineEdit_3.setObjectName(u"proj_loc")

        self.gridLayout.addWidget(self.lineEdit_3, 7, 0, 1, 2)

        self.label_7 = QLabel(self.widget)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout.addWidget(self.label_7, 7, 2, 1, 1)

        self.radioButton = QRadioButton(self.widget)
        self.radioButton.setObjectName(u"radioButton")

        self.gridLayout.addWidget(self.radioButton, 8, 0, 1, 2)

        self.radioButton_2 = QRadioButton(self.widget)
        self.radioButton_2.setObjectName(u"radioButton_2")

        self.gridLayout.addWidget(self.radioButton_2, 9, 0, 1, 2)

        self.verticalSpacer_2 = QSpacerItem(20, 18, QSizePolicy.Policy.Minimum,  QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_2, 10, 1, 1, 1)

        self.lineEdit_4 = QLineEdit(self.widget)
        self.lineEdit_4.setObjectName(u"cumulative_ic")

        self.gridLayout.addWidget(self.lineEdit_4, 11, 0, 1, 2)

        self.label_8 = QLabel(self.widget)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout.addWidget(self.label_8, 11, 2, 1, 1)

        self.lineEdit_5 = QLineEdit(self.widget)
        self.lineEdit_5.setObjectName(u"cumulative_fos")

        self.gridLayout.addWidget(self.lineEdit_5, 12, 0, 1, 2)

        self.label_9 = QLabel(self.widget)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout.addWidget(self.label_9, 12, 2, 1, 1)

        self.lineEdit_6 = QLineEdit(self.widget)
        self.lineEdit_6.setObjectName(u"add_req1")

        self.gridLayout.addWidget(self.lineEdit_6, 13, 0, 1, 2)

        self.label_10 = QLabel(self.widget)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout.addWidget(self.label_10, 13, 2, 1, 1)

        self.radioButton_3 = QRadioButton(self.widget)
        self.radioButton_3.setObjectName(u"radioButton_3")

        self.gridLayout.addWidget(self.radioButton_3, 14, 0, 1, 2)

        self.verticalSpacer_3 = QSpacerItem(20, 18, QSizePolicy.Policy.Minimum,  QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_3, 15, 1, 1, 1)

        self.lineEdit_7 = QLineEdit(self.widget)
        self.lineEdit_7.setObjectName(u"add_req2")

        self.gridLayout.addWidget(self.lineEdit_7, 16, 0, 1, 2)

        self.label_11 = QLabel(self.widget)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout.addWidget(self.label_11, 16, 2, 1, 1)

        self.lineEdit_8 = QLineEdit(self.widget)
        self.lineEdit_8.setObjectName(u"add_req3")

        self.gridLayout.addWidget(self.lineEdit_8, 17, 0, 1, 2)

        self.label_12 = QLabel(self.widget)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout.addWidget(self.label_12, 17, 2, 1, 1)

        self.lineEdit_9 = QLineEdit(self.widget)
        self.lineEdit_9.setObjectName(u"add_req4")

        self.gridLayout.addWidget(self.lineEdit_9, 18, 0, 1, 2)

        self.label_13 = QLabel(self.widget)
        self.label_13.setObjectName(u"label_13")

        self.gridLayout.addWidget(self.label_13, 18, 2, 1, 1)

        self.radioButton_4 = QCheckBox(self.widget)
        self.radioButton_4.setObjectName(u"radioButton_4")

        self.gridLayout.addWidget(self.radioButton_4, 19, 0, 1, 2)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum,  QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_4, 20, 1, 1, 1)

        self.pushButton = QPushButton(self.widget)
        self.pushButton.setObjectName(u"Load Project Requirements")
        self.pushButton.clicked.connect(self.load_proj_requirements)

        self.gridLayout.addWidget(self.pushButton, 21, 0, 1, 1)

        self.pushButton_2 = QPushButton(self.widget)
        self.pushButton_2.setObjectName(u"Save Project Requirements")

        self.pushButton_2.clicked.connect(self.save_project_requirements)

        self.gridLayout.addWidget(self.pushButton_2, 21, 1, 1, 2)

        self.retranslateUi(Widget)

        QMetaObject.connectSlotsByName(Widget)

    def load_proj_requirements(self):
        """
        We will always save the proj_requirements in
        @TODO We need to implemetent lock and unlock for editing. Itrs annyoing
        @TODO: Project Requirements should also load check boxes, and radio buttons
        @TODO: If you create a new proejct and you dont define the proj requirements, you cannot load it back. Throws file not found error
        """
        # ffp = os.getcwd()
        # filename, _ = QFileDialog.getOpenFileName(self, 'Open File', ffp+ '/project/project_settings', '*.json')
        # print(filename)

        filename = self.main.ffp.proj_requirements + 'requirements.json'

        if not os.path.exists(filename):
            return

        with open(filename) as f:
            proj_req = json.load(f)
        self.lineEdits = self.widget.findChildren(QLineEdit)

        for lineEdit in self.lineEdits:
            try:
                lineEdit.setText(str(proj_req[lineEdit.objectName()]))
                # lineEdit.setReadOnly(True)
            except KeyError:
                pass

        self.main.proj_requirements = proj_req
        print(proj_req)




    def save_project_requirements(self):
        self.lineEdits = self.widget.findChildren(QLineEdit)

        proj_req = parse_proj_requirements(self.lineEdits) #Everything is saved as txt

        # ffp = os.getcwd()
        # name = '/project/project_settings/'
        # path = ffp + name
        # if not os.path.exists(path):
        #     os.makedirs(path)

        with open(self.main.ffp.proj_requirements + 'requirements.json', 'w') as f:
            json.dump(proj_req, f)

        self.main.proj_requirements = proj_req
        #Select all qline edits





    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Mw", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Pga.", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Gwl", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Scf", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"ProjName", None))
        self.label_6.setText(QCoreApplication.translate("Dialog", u"ProjNum", None))
        self.label_7.setText(QCoreApplication.translate("Dialog", u"ProjLoc", None))
        self.radioButton.setText(QCoreApplication.translate("Dialog", u"Robertston&Wride1997", None))
        self.radioButton_2.setText(QCoreApplication.translate("Dialog", u"Boulanger&Idriss2014", None))
        self.label_8.setText(QCoreApplication.translate("Dialog", u"Cumulative IC(no.)", None))
        self.label_9.setText(QCoreApplication.translate("Dialog", u"Cumulative FOS(no.)", None))
        self.label_10.setText(QCoreApplication.translate("Dialog", u"TextLabel", None))
        self.radioButton_3.setText(QCoreApplication.translate("Dialog", u"RadioButton", None))
        self.label_11.setText(QCoreApplication.translate("Dialog", u"TextLabel", None))
        self.label_12.setText(QCoreApplication.translate("Dialog", u"TextLabel", None))
        self.label_13.setText(QCoreApplication.translate("Dialog", u"TextLabel", None))
        self.radioButton_4.setText(QCoreApplication.translate("Dialog", u"RadioButton", None))
        self.pushButton.setText(QCoreApplication.translate("Dialog", u"Load Requirements", None))
        self.pushButton_2.setText(QCoreApplication.translate("Dialog", u"Save Requirements", None))
    # retranslateUi


# Create the application instance
# # app = QApplication(sys.argv)
# #
# # # Create the widget window
# # # widget = Ui_Widget()
# # widget = Ui_WidgetGrid()
# #
# # # Show the widget window
# # widget.show()
# #
# # # Start the event loop
# sys.exit(app.exec())
