from PyQt6.QtWidgets import *
from PyQt6.uic import loadUi
import sys



class HomeQT2(QDialog):
    def __init__(self, main_window_ref, parent = None):
        super(HomeQT2, self).__init__(parent)
        # loadUi('uis/home2.ui', self)
        # loadUi('uis/convert2.ui', self)
        # loadUi('uis/projreqs2.ui', self)

        # loadUi('uis/load2.ui', self)
        loadUi('uis/calculations2.ui', self)

        self.main = main_window_ref
        labels = self.findChildren(QLabel)



        # self.treeview = TreeView()
        # self.tableWidget = PDWidget()


        # self.setCentralWidget()


#
# app = QApplication(sys.argv)
# main = HomeQT2(123)
#
# with open("uis/white_theme.qss", "r") as f:
#     _style = f.read()
#     app.setStyleSheet(_style)
#
#
# main.show()
# sys.exit(app.exec())