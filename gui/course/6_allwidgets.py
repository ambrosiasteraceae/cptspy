# vIn Qt (and most User Interfaces) ‘widget’ is the name given to a component of the UI that the user can interact
# with. User interfaces are made up of multiple widgets, arranged within the window.


import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDateEdit,
    QDateTimeEdit,
    QDial,
    QDoubleSpinBox,
    QFontComboBox,
    QLabel,
    QLCDNumber,
    QLineEdit,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QSlider,
    QSpinBox,
    QTimeEdit,
    QVBoxLayout,
    QWidget,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        widgets = [QCheckBox,
                   QComboBox,
                   QDateEdit,
                   QDateTimeEdit,
                   QDial,
                   QDoubleSpinBox,
                   QFontComboBox,
                   QLabel,
                   QLCDNumber,
                   QLineEdit,
                   QMainWindow,
                   QProgressBar,
                   QPushButton,
                   QRadioButton,
                   QSlider,
                   QSpinBox,
                   QTimeEdit]

        mwidget = QWidget()
        layout = QVBoxLayout()


        for widget in widgets:
            layout.addWidget(widget())


        mwidget.setLayout(layout)

        self.setCentralWidget(mwidget)


app = QApplication(sys.argv)
main = MainWindow()

main.show()

app.exec()