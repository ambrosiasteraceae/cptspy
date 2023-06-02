from PyQt6 import QtCore, QtGui, QtWidgets


class widgetB(QtWidgets.QWidget):

    procDone = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(widgetB, self).__init__(parent)

        self.lineEdit = QtWidgets.QLineEdit(self)
        self.button = QtWidgets.QPushButton("Send Message to A", self)
        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.addWidget(self.lineEdit)
        self.layout.addWidget(self.button)

        self.button.clicked.connect(self.on_button_clicked)

    @QtCore.pyqtSlot()
    def on_button_clicked(self):
        self.procDone.emit(self.lineEdit.text())

    @QtCore.pyqtSlot(str)
    def on_procStart(self, message):
        self.lineEdit.setText("From A: " + message)

        self.raise_()


class widgetA(QtWidgets.QWidget):
    procStart = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(widgetA, self).__init__(parent)

        self.lineEdit = QtWidgets.QLineEdit(self)
        self.lineEdit.setText("Hello!")

        self.button = QtWidgets.QPushButton("Send Message to B", self)
        self.button.clicked.connect(self.on_button_clicked)

        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.addWidget(self.lineEdit)
        self.layout.addWidget(self.button)

    @QtCore.pyqtSlot()
    def on_button_clicked(self):
        self.procStart.emit(self.lineEdit.text())

    @QtCore.pyqtSlot(str)
    def on_widgetB_procDone(self, message):
        self.lineEdit.setText("From B: " + message)

        self.raise_()


class mainwindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(mainwindow, self).__init__(parent)

        self.button = QtWidgets.QPushButton("Click Me", self)
        self.button.clicked.connect(self.on_button_clicked)

        self.setCentralWidget(self.button)

        self.widgetA = widgetA()
        self.widgetB = widgetB()

        self.widgetA.procStart.connect(self.widgetB.on_procStart)
        self.widgetB.procDone.connect(self.widgetA.on_widgetB_procDone)

    @QtCore.pyqtSlot()
    def on_button_clicked(self):
        self.widgetA.show()
        self.widgetB.show()

        self.widgetA.raise_()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    main = mainwindow()
    main.show()
    sys.exit(app.exec())