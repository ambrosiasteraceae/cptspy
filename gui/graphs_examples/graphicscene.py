import pyqtgraph as pg
from PyQt6.QtWidgets import QGraphicsScene, QGraphicsItem
from PyQt6.QtWidgets import *
from PyQt6.QtCore import QPointF, QRectF
from PyQt6.QtGui import *
from pyqtgraph import PlotWidget
import sys
import pyqtgraph as pg
from PyQt6.QtCore import Qt

class GraphicsView(QGraphicsView):
    def __init__(self, scene):
        super().__init__(scene)
        self._zoom = 0
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            factor = 1.25
            self._zoom += 1
        else:
            factor = 0.8
            self._zoom -= 1

        if self._zoom > 0:
            self.scale(factor, factor)
        elif self._zoom == 0:
            self.setTransform(QTransform())
        else:
            self._zoom = 0

class CustomScene(QGraphicsScene):
    def __init__(self):
        super().__init__()
        self.poly1 = QPolygonF([QPointF(0, 0), QPointF(0, 10), QPointF(10, 10), QPointF(10, 0)])
        self.addPolygon(self.poly1)
        self.QBrush = pg.mkBrush(255, 0, 0, 100)

    def mousePressEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        print("Mouse Pressed")
        print(event.scenePos().x(), event.scenePos().y())

        if self.itemAt(event.scenePos().x(), event.scenePos().y(),QTransform()):
            print("Item Found")
            self.itemAt(event.scenePos().x(), event.scenePos().y(),QTransform()).setBrush(self.QBrush)
            self.update()


        # print()

class GSceneQT(PlotWidget):
    def __init__(self):
        self.scene = CustomScene()


app = QApplication(sys.argv)
obj = GSceneQT()
obj.view.show()

sys.exit(app.exec())

self.view = GraphicsView(self.scene)
# self.setCentralWidget(self.view)
