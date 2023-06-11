from PyQt6.QtWidgets import *
from PyQt6 import QtCore


class RedMessageBox(QMessageBox):
    def __init__(self, msg):
        super(RedMessageBox, self).__init__()
        self.setWindowTitle("Error")
        self.setText(msg)
        # Apply styles using style sheets
        self.setStyleSheet("""
            QMessageBox {
                background-color: #fcdbe1;
            }

            }
            QLabel {
                color: #d86f85;
                font-weight: bold;
                font-size: 15px;
                background-color: transparent
            }
            QPushButton {
                background-color: #d86f85;
                color: white;
                font-weight: bold;
                font-size: 15px;
                border-color : 2px solid #d86f85;
            }
        """)
        self.exec()



class GreenMessageBox(QMessageBox):
    def __init__(self, msg):
        super(GreenMessageBox, self).__init__()
        self.setText(msg)
        # Apply styles using style sheets
        self.setStyleSheet("""
            QMessageBox {
                background-color: white;
            }
            QLabel {
                color: #3cB043;
                font-weight: bold;
                font-size: 15px;
            }
            QPushButton {
                background-color: white;
                color: #3cB043;
                font-weight: bold;
                font-size: 15px;
                border: 1px solid #3cB043;
            }
        """)
        self.exec()


