import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import Qt
from dataclasses import dataclass

@dataclass
class Grid():
    #name, grid-id, size, x, y, z
    name: str
    coords: tuple
    tests: list

    def __repr__(self):
        return f'{self.name}'

    def insert(self,obj):
        if isinstance(obj, Test):
            self.tests.append(obj)

            if len(self.tests) ==0:
                pass
            else:
                setattr(self, 'test_count', len(self.tests))

            print(obj)
            return
        print('Cannot insert a Non-Test obj')

@dataclass
class Test():
    #name,east,north
    name: str
    contractor: str
    easting: str
    northing: float
    date: float
    length: float
    summary : object

    def __repr__(self):
        return f'{self.name}'



cpt1 = Test('AK47-1a', 1, 1, 1,1,1,None)
cpt2 = Test('AK47-1d', 2, 2, 2,2,2,None)

grid = Grid('AK47', (1, 1), [])
grid2 = Grid('MK74', (1, 1), [])

grid.insert(cpt1)
grid.insert(cpt2)
# grid.insert(cpt2.name, cpt2)



class TreeGridItem():
    def __init__(self, obj):
        super().__init__()
        self.grid = QStandardItem(obj.name)

        for k,v in grid.__dict__.items():
            if isinstance(v, list):
                self.parent = QStandardItem('Tests')
                self.grid.appendRow(self.parent)
                for test in v:
                    self.test = QStandardItem(test.name)
                    for test_k, test_v in test.__dict__.items():
                        if isinstance(test_v, object):
                            self.test.appendRow([QStandardItem(test_k),QStandardItem(str(test_v))])
                        else:
                            self.test.appendRow([QStandardItem(test_k),QStandardItem(str(test_v))])

                    self.parent.appendRow(self.test)
            else:
                # print(k,v)
                self.grid.appendRow([QStandardItem(k),QStandardItem(str(v))])

# class TreeGridItem():
#     def __init__(self, obj):
#         self.parent = QStandardItem(obj.name)
#         self.add_attributes(obj)
#         self.add_tests(obj)
#
#     def add_attributes(self, obj):
#         attributes = [(k, v) for k, v in obj.__dict__.items() if k != "tests"]
#         self.add_items(self.parent, attributes)
#
#     def add_tests(self, obj):
#         tests = obj.tests
#         for test in tests:
#             test_item = QStandardItem(test.name)
#             test_attributes = [(k, v) for k, v in test.__dict__.items()]
#             self.add_items(test_item, test_attributes)
#             self.parent.appendRow(test_item)
#
#     def add_items(self, parent, items):
#         for key, value in items:
#             parent.appendRow([QStandardItem(str(key)), QStandardItem(str(value))])


class AppDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt6 QTreeView @ stuvel.eu")
        self.resize(800, 600)
        treeView = QTreeView()
        self.treemodel = QStandardItemModel()

        self.button = QPushButton('Insert')
        self.button.clicked.connect(self.add_grid)

        self.treemodel.setHorizontalHeaderLabels(['Name', 'Value'])
        treeView.setModel(self.treemodel)

        grid_item = TreeGridItem(grid)
        self.treemodel.appendRow(grid_item.grid)

        #define a vertical layout with the treeView and button
        layout = QVBoxLayout()
        layout.addWidget(treeView)
        layout.addWidget(self.button)
        
        # self.setCentralWidget(treeView)
        self.setLayout(layout)
        

    def add_grid(self):
         self.treemodel.appendRow(TreeGridItem(grid2).grid)
         
        
        


app = QApplication(sys.argv)
demo = AppDemo()
demo.show()
sys.exit(app.exec())
