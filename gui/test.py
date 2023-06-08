
import sys
from PyQt6.QtWidgets import *
from PyQt6.uic import loadUi

class Someting(QWidget):
    def __init__(self):
        super(Someting, self).__init__()
        loadUi('uis/overview.ui', self)

        labels = self.findChildren(QLabel)
        print(labels[0].setText('AAASS'))

        self.setCentralWidget()

    def setCentralWidget(self):
        pass


app = QApplication(sys.argv)
main = Someting()

with open("uis/white_theme.qss", "r") as f:
    _style = f.read()
    app.setStyleSheet(_style)


main.show()
sys.exit(app.exec())


