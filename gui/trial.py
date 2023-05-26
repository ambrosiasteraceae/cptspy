import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QPushButton, QFileDialog, QListView
from PyQt6.QtCore import Qt, QStringListModel, QMimeData
from PyQt6.QtGui import QStandardItemModel, QStandardItem, QDrag

class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()

        self.setWindowTitle("File Uploader")
        self.setGeometry(100, 100, 600, 400)

        self.tab_widget = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()

        self.tab_widget.addTab(self.tab1, "Tab 1")
        self.tab_widget.addTab(self.tab2, "Tab 2")
        self.tab_widget.addTab(self.tab3, "Tab 3")

        self.tab1_layout = QVBoxLayout()
        self.tab1.setLayout(self.tab1_layout)

        self.upload_file_btn = QPushButton("Upload File")
        self.upload_file_btn.clicked.connect(self.upload_file)

        self.upload_folder_btn = QPushButton("Upload Folder")
        self.upload_folder_btn.clicked.connect(self.upload_folder)

        self.list_view = QListView()
        self.model = QStandardItemModel(self.list_view)
        self.list_view.setModel(self.model)
        self.list_view.setDragEnabled(True)
        self.list_view.setAcceptDrops(True)
        self.list_view.setDragEnabled(True)

        self.tab1_layout.addWidget(self.upload_file_btn)
        self.tab1_layout.addWidget(self.upload_folder_btn)
        self.tab1_layout.addWidget(self.list_view)

        self.setCentralWidget(self.tab_widget)

        self.print_paths_btn = QPushButton("Print File Paths")
        self.print_paths_btn.clicked.connect(self.print_file_paths)
        self.tab1_layout.addWidget(self.print_paths_btn)

    def upload_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open file', '', "Excel Files (*.xlsx)")
        if file_name:
            item = QStandardItem(file_name)
            self.model.appendRow(item)

    def upload_folder(self):
        folder_name = QFileDialog.getExistingDirectory(self, 'Open Folder')
        if folder_name:
            for file_name in os.listdir(folder_name):
                if file_name.endswith('.xlsx'):
                    item = QStandardItem(os.path.join(folder_name, file_name))
                    self.model.appendRow(item)

    def print_file_paths(self):
        for i in range(self.model.rowCount()):
            item = self.model.item(i)
            print(item.text())


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = MyWindow()
    main.show()

    sys.exit(app.exec())
