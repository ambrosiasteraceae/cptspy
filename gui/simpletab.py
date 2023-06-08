from PyQt6.QtWidgets import QMessageBox, QApplication
from PyQt6.QtGui import QFont

app = QApplication([])

# Create a QMessageBox
msg_box = QMessageBox()
msg_box.setWindowTitle("Styled QMessageBox Example")
msg_box.setText("This is a styled QMessageBox!")

# Apply styles using style sheets
msg_box.setStyleSheet("""
    QMessageBox {
        background-color: #fcdbe1;
    }
    QLabel {
        color: #d86f85;
        font-weight: bold;
        font-size: 15px;
    }
    QPushButton {
        background-color: #fcdbe1;
        color: #d86f85;
        font-weight: bold;
        font-size: 15px;
    }
""")

# Apply font settings
font = QFont()
font.setPointSize(15)
msg_box.setFont(font)
# Show the QMessageBox
msg_box.exec()