import os
import json

from PyQt6.QtWidgets import *
from PyQt6.QtGui import QDoubleValidator
from PyQt6.QtGui import *
from PyQt6.uic import loadUi
from extras import GreenMessageBox, RedMessageBox

def build_tree_model(data):
    def add_items(parent_item, data):
        if isinstance(data, dict):
            for key, value in data.items():
                item = QStandardItem(str(key))
                parent_item.appendRow(item)
                add_items(item, value)
        elif isinstance(data, list):
            for value in data:
                item = QStandardItem(str(value))
                parent_item.appendRow(item)
                add_items(item, value)
        else:
            item = QStandardItem(str(data))
            parent_item.appendRow(item)

    model = QStandardItemModel()
    add_items(model.invisibleRootItem(), data)
    return model


def load_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def parse_proj_requirements(line_edits):
    proj_req = {}
    for lineEdit in line_edits:
        try:
            val = int(lineEdit.text())
        except ValueError:
            try:
                val = float(lineEdit.text())
            except ValueError:
                val = lineEdit.text()

        proj_req[lineEdit.objectName()] = val
    return proj_req


class ProjReqWidget(QDialog):
    def __init__(self, main_window_ref,parent=None):
        super(ProjReqWidget, self).__init__(parent)
        self.main = main_window_ref

        loadUi('uis/projreqs2.ui', self)

        self.save_settings_btn.clicked.connect(self.save_project_requirements)
        self.load_settings_btn.clicked.connect(self.load_proj_requirements)
        self.refresh_json_btn.clicked.connect(self.refresh_action)

        self.previous_btn.clicked.connect(self.main.tab_widget.previous)
        self.next_btn.clicked.connect(self.main.tab_widget.next)

        onlyFloat = QDoubleValidator()





    def refresh_action(self):
        try:
            self.data = load_json_file(self.main.ffp.proj_requirements + 'requirements.json')
        except FileNotFoundError:
            RedMessageBox('No requirements.json file found! Maybe you forgot to save the file?')
            return
        model = build_tree_model(self.data)
        self.proj_tree.setModel(model)
        self.proj_tree.expandAll()
        self.proj_tree.show()

    def load_proj_requirements(self):


        filename = self.main.ffp.proj_requirements + 'requirements.json'

        if not os.path.exists(filename):
            return

        with open(filename) as f:
            proj_req = json.load(f)

        self.lineEdits = self.findChildren(QLineEdit)

        for lineEdit in self.lineEdits:
            try:
                lineEdit.setText(str(proj_req[lineEdit.objectName()]))
                # lineEdit.setReadOnly(True)
            except KeyError:
                pass

        self.main.proj_requirements = proj_req


    def save_project_requirements(self):
        self.lineEdits = self.findChildren(QLineEdit)

        proj_req = parse_proj_requirements(self.lineEdits)

        with open(self.main.ffp.proj_requirements + 'requirements.json', 'w') as f:
            json.dump(proj_req, f)

        self.main.proj_requirements = proj_req

        GreenMessageBox('Project requirements are succesfully saved!')

