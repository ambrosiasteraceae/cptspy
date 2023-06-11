
import pandas as pd
from PyQt6.QtCore import Qt, QAbstractTableModel, QModelIndex, QVariant
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QColor

class PandasModel(QAbstractTableModel):
    def __init__(self, df=pd.DataFrame(), parent=None):
        QAbstractTableModel.__init__(self, parent=parent)
        self._df = df

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role != Qt.ItemDataRole.DisplayRole:
            return QVariant()

        if orientation == Qt.Orientation.Horizontal:
            try:
                return self._df.columns.tolist()[section]
            except (IndexError,):
                return QVariant()
        elif orientation == Qt.Orientation.Vertical:
            try:
                # return self.df.index.tolist()
                return self._df.index.tolist()[section]
            except (IndexError,):
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
        self._df.sort_values(colname, ascending=order == Qt.SortOrder.AscendingOrder, inplace=True)
        self._df.reset_index(inplace=True, drop=True)
        self.layoutChanged.emit()

class PDWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=None)
        vLayout = QVBoxLayout(self)
        hLayout = QHBoxLayout()

        vLayout.addLayout(hLayout)
        self.pandasTv = QTableView(self)
        vLayout.addWidget(self.pandasTv)

        self.pandasTv.setSortingEnabled(True)

        class CustomDelegate(QStyledItemDelegate):
            def paint(self, painter, option, index):
                # Custom painting code here
                if index.row() % 2 == 0:
                    painter.fillRect(option.rect, QColor(220, 220, 220))  # Alternate row color 1
                else:
                    painter.fillRect(option.rect, QColor(255, 255, 255))  # Alternate row color 2

                # Call the base class paint() method to handle other painting tasks
                super().paint(painter, option, index)

        # delegate = CustomDelegate(self)
        # self.pandasTv.setItemDelegate(delegate)

    def loadFile(self):
        # if fileName is None:
        fileName, _ = QFileDialog.getOpenFileName(self, "Open File", "", "CSV Files (*.csv)");
        # self.pathLE.setText(fileName)
        # if df is None:
        df = pd.read_csv(fileName, delimiter=';')
        model = PandasModel(df)
        self.pandasTv.setModel(model)

    def loadDF(self, path, df):

        model = PandasModel(df)
        self.pandasTv.setModel(model)

    def updateView(self, df):
        # Get the existing model
        model = self.pandasTv.model()

        # Set a new DataFrame to the model
        model._df = df

        # Refresh the view
        model.layoutChanged.emit()
