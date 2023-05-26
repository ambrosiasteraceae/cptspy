import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")
        button = QPushButton('Press Me!')


        #2
        button.clicked.connect(self.the_button_was_clicked)

        #1
        # button.setCheckable(True)
        # button.clicked.connect(self.the_button_was_clicked)
        # button.clicked.connect(self.the_button_was_toggled)

        self.setCentralWidget(button)

    def the_button_was_clicked(self):
        print('CLICKED')

    def the_button_was_toggled(self,checked):
        self.button_is_checked = checked
        print(self.button_is_checked)

    def the_button_was_clicked(self):
        self.button.setText('You already clickedbme')
        self.button.setEnabled(False)

        self.setWindowTitle('My one shot')



app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()