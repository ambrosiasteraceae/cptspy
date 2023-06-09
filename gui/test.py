
import sys
from PyQt6.QtWidgets import *
from PyQt6.uic import loadUi
from home import TreeView
from projectinfo import PDWidget
from home import TreeView




class SomethingQT(QWidget):
    def __init__(self, main_window_ref, parent = None):
        super(SomethingQT, self).__init__(parent)
        loadUi('uis/overview.ui', self)

        self.main = main_window_ref
        labels = self.findChildren(QLabel)



        # self.treeview = TreeView()
        # self.tableWidget = PDWidget()
        self.merge_dfs.clicked.connect(self.load_fucking_tv)
        self.merge_dfs.setText('Mthfcker')
        self.label_4.setText('Mthfcker')

        print(labels[0].setText('AAASS'))

        self.setCentralWidget()

    def setCentralWidget(self):
        pass

    def load_fucking_tv(self):
        print('button has been pressed')
        self.tableWidget.loadDF('123', self.main.hdf)
        print(self.main.hdf.head())

# app = QApplication(sys.argv)
# main = SomethingQT(123)
#
# with open("uis/white_theme.qss", "r") as f:
#     _style = f.read()
#     app.setStyleSheet(_style)
#
#
# main.show()
# sys.exit(app.exec())
#

