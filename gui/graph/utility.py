import pyqtgraph as pg
from PyQt6.QtWidgets import QGraphicsPolygonItem


class CustomGrid(QGraphicsPolygonItem):
    def __init__(self, *args, graph_ref, gridobj, **kwargs):
        super().__init__(*args, **kwargs)
        # self.setAcceptHoverEvents(True)
        self.graph = graph_ref
        self.grid_obj = gridobj

    def hoverEnterEvent(self, event):
        print('Mouse entered at: ', event.screenPos(), self.grid_obj)

    def mousePressEvent(self, event):
        self.setBrush(pg.mkBrush(0, 255, 0, 100))
        self.graph.container[self.grid_obj.name] = self.polygon()
        print(len(self.graph.container))
        # super().mousePressEvent(event)
        print('Bounding area: ', self.polygon().boundingRect())
        self.graph.insert_grid(self.grid_obj)