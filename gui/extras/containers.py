from dataclasses import dataclass
from PyQt6.QtGui import QStandardItem

@dataclass
class Grid:
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
class Test:
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


class TreeGridItem:
    def __init__(self, obj):
        self.parent = QStandardItem(obj.name)
        self.add_attributes(obj)
        self.add_tests(obj)

    def add_attributes(self, obj):
        attributes = [(k, v) for k, v in obj.__dict__.items() if k != "tests"]
        self.add_items(self.parent, attributes)

    def add_tests(self, obj):
        tests = obj.tests
        for test in tests:
            test_item = QStandardItem(test.name)
            test_attributes = [(k, v) for k, v in test.__dict__.items()]
            self.add_items(test_item, test_attributes)
            self.parent.appendRow(test_item)

    def add_items(self, parent, items):
        for key, value in items:
            parent.appendRow([QStandardItem(str(key)), QStandardItem(str(value))])

