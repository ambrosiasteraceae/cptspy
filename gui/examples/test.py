
import sys
from PyQt6.QtWidgets import *
from PyQt6.uic import loadUi
import pandas as pd

from extras import PDWidget, TreeView


class SomethingQT(QWidget):
    def __init__(self, main_window_ref, parent = None):
        super(SomethingQT, self).__init__(parent)
        loadUi('uis/overview2.ui', self)

        self.main = main_window_ref
        labels = self.findChildren(QLabel)
        self.df = pd.read_excel('C:/Users/dragos/Documents/GitHub/cptspy/gui/hudayriyat/summary/Results.xlsx')

        # self.table.setVisible(True)

        # self.treeview = TreeView()
        # self.table = PDWidget()
        self.merge_dfs.clicked.connect(self.load_fucking_tv)
        self.merge_dfs.setText('Mthfcker')
        self.label_4.setText('Mthfcker')

        print(labels[0].setText('AAASS'))
    #     self.setCentralWidget()
    #
    # def setCentralWidget(self):
    #     pass


    def load_fucking_tv(self):
        print('button has been pressed')
        # print(self.df.head())
        self.table.loadDF('123', self.df)
        # self.table.update()

#
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
# #
# #
