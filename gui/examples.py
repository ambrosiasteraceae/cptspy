import pyqtgraph as pg
from PyQt6.QtWidgets import *


def myfunc():
    print(2)

app = QApplication([])

main = QWidget()
main.setWindowTitle('PyQtGraph example: PlotWidget')


btn = QPushButton('Click me')
btn.clicked.connect(lambda: print('Clicked!'))

ltn = QPushButton('Print 2')
ltn.clicked.connect(myfunc)

layout = QGridLayout()

main.setLayout(layout)
layout.addWidget(btn,0,0)
layout.addWidget(ltn,0,1)

main.show()

app.exec()

