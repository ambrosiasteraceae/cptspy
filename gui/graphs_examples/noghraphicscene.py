import sys
from PyQt6.QtWidgets import QApplication
import pyqtgraph as pg
from pyqtgraph import PlotWidget, PlotDataItem
from PyQt6.QtCore import QPointF, QRectF
from PyQt6.QtGui import QPolygonF, QBrush, QColor

class CustomPlot(PlotWidget):
    def __init__(self):
        super().__init__()
        self.poly1 = QPolygonF([QPointF(0, 0), QPointF(0, 10), QPointF(10, 10), QPointF(10, 0)])
        self.plotItem = self.getPlotItem()  # Get the PlotItem of the PlotWidget
        self.plotItem.addItem(self.poly1)  # Add the polygon to the PlotItem

    # def mousePressEvent(self, event):
    #     pos = self.plotItem.vb.mapSceneToView(event.pos())  # Map the mouse position to the coordinate system of the PlotItem
    #     print("Mouse Pressed")
    #     print(pos.x(), pos.y())
    #
    #     # Check if the mouse position is inside the polygon
    #     if self.poly1.contains(QPointF(pos.x(), pos.y())):
    #         print("Item Found")
    #         self.plotItem.plot(self.poly1, fillLevel=0, brush=(255, 0, 0, 100))  # Redraw the polygon with the new color

app = QApplication(sys.argv)
customPlot = CustomPlot()
customPlot.show()
sys.exit(app.exec())
