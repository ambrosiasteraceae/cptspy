# importing Qt widgets
from PyQt6.QtWidgets import *

# importing system
import sys

# importing numpy as np
import numpy as np

# importing pyqtgraph as pg
import pyqtgraph as pg
from PyQt6.QtGui import *
from PyQt6.QtCore import *



# Image View class
class ImageView(pg.ImageView):
    # constructor which inherit original
    # ImageView
    def __init__(self, *args, **kwargs):
        pg.ImageView.__init__(self, *args, **kwargs)


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        # setting title
        self.setWindowTitle("PyQtGraph")

        # setting geometry
        self.setGeometry(100, 100, 600, 500)

        # icon
        icon = QIcon("skin.png")

        # setting icon to the window
        self.setWindowIcon(icon)

        # calling method
        self.UiComponents()

        # showing all the widgets
        self.show()

    # method for components
    def UiComponents(self):
        # creating a widget object
        widget = QWidget()

        # creating a label
        label = QLabel("Geeksforgeeks Graph Item")

        # setting minimum width
        label.setMinimumWidth(67)

        # making label do word wrap
        label.setWordWrap(True)

        # setting configuration options
        pg.setConfigOptions(antialias=True)
        # pg.setConfigOptions(antialias=True)
        pg.setConfigOption('useOpenGL', True)

        # creating graphics layout widget
        win = pg.GraphicsLayoutWidget()

        # adding view box to the graphic layout widget
        view = win.addViewBox()

        # lock the aspect ratio
        view.setAspectLocked()

        # creating a graph item
        graph_item = pg.GraphItem()

        # adding graph item to the view box
        view.addItem(graph_item)

        # Define positions of nodes
        pos = np.array([[x, y] for x in range(100) for y in range(100)])

        # Define the set of connections in the graph
        adj = np.array([[i, i + 1] for i in range(999)])

        # Define the symbol to use for each node (this is optional)
        symbols = ['s' for _ in range(10000)]

        # Define the line style for each connection (this is optional)
        lines = np.array(
            [(255, 0, 0, 255, 1) for _ in range(999)],
            dtype=[('red', np.ubyte), ('green', np.ubyte), ('blue', np.ubyte), ('alpha', np.ubyte), ('width', float)]
        )

        # Update the graph
        graph_item.setData(pos=pos, adj=adj, pen=lines, size=0.25, symbol=symbols, pxMode=False)

        # Creating a grid layout
        layout = QGridLayout()

        # minimum width value of the label
        label.setMinimumWidth(130)

        # setting this layout to the widget
        widget.setLayout(layout)

        # adding label in the layout
        layout.addWidget(label, 1, 0)

        # plot window goes on right side, spanning 3 rows
        layout.addWidget(win, 0, 1, 3, 1)

        # setting this widget as central widget of the main window
        self.setCentralWidget(widget)

        # getting rectangle covered for graph item
        value = graph_item.boundingRect()

        # setting text to the label
        label.setText("Rectangle : " + str(value))


# create pyqt6 app
app = QApplication(sys.argv)

# create the instance of our Window
window = Window()

# start the app
sys.exit(app.exec())
