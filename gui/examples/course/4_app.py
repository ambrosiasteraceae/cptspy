import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QTextEdit


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.label = QLabel("Click in this window")
        self.setCentralWidget(self.label)
        self.setMouseTracking(True)

    def mouseMoveEvent(self, e):
        self.label.setText("mouseMoveEvent")

    def mousePressEvent(self, e):
        self.label.setText("mousePressEvent")

    def mouseReleaseEvent(self, e):
        self.label.setText("mouseReleaseEvent")

    def mouseDoubleClickEvent(self, e):
        self.label.setText("mouseDoubleClickEvent")



    # def mousePressEvent(self, e):
    #     if e.button() == Qt.LeftButton:
    #         # handle the left-button press in here
    #         self.label.setText("mousePressEvent LEFT")
    #
    #     elif e.button() == Qt.MiddleButton:
    #         # handle the middle-button press in here.
    #         self.label.setText("mousePressEvent MIDDLE")
    #
    #     elif e.button() == Qt.RightButton:
    #         # handle the right-button press in here.
    #         self.label.setText("mousePressEvent RIGHT")
    #
    # def mouseReleaseEvent(self, e):
    #     if e.button() == Qt.LeftButton:
    #         self.label.setText("mouseReleaseEvent LEFT")
    #
    #     elif e.button() == Qt.MiddleButton:
    #         self.label.setText("mouseReleaseEvent MIDDLE")
    #
    #     elif e.button() == Qt.RightButton:
    #         self.label.setText("mouseReleaseEvent RIGHT")
    #
    # def mouseDoubleClickEvent(self, e):
    #     if e.button() == Qt.LeftButton:
    #         self.label.setText("mouseDoubleClickEvent LEFT")
    #
    #     elif e.button() == Qt.MiddleButton:
    #         self.label.setText("mouseDoubleClickEvent MIDDLE")
    #
    #     elif e.button() == Qt.RightButton:
    #         self.label.setText("mouseDoubleClickEvent RIGHT")

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
