import pyqtgraph as pg
import numpy as np
from PyQt6.QtWidgets import QGraphicsPathItem


from PyQt6.QtWidgets import *
from PyQt6.uic import loadUi
import sys
from pyqtgraph import PlotWidget


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow,self).__init__()


        plt = pg.plot()

        lines = 1000
        points = 100
        x = np.empty((lines, points))
        x[:] = np.arange(points)
        y = np.random.normal(size=(lines, points))
        connect = np.ones((lines, points), dtype=np.ubyte)
        connect[:,-1] = 0  #  disconnect segment between lines
        path = pg.arrayToQPath(x.reshape(lines*points), y.reshape(lines*points), connect.reshape(lines*points))
        item = QGraphicsPathItem(path)
        item.setPen(pg.mkPen('w'))
        plt.addItem(item)

        # self.setCentralWidget(plt)


app = QApplication(sys.argv)
main = MainWindow()



main.show()
sys.exit(app.exec())
