from dataclasses import dataclass
from PyQt6.QtGui import QStandardItem
from shapely import Polygon

@dataclass
class Grid:
    # name, grid-id, size, x, y, z
    name: str
    bounds: tuple
    polygon: Polygon
    contained_tests: set
    tests: list

    def __repr__(self):
        return f'{self.name}'

    def insert(self, test):
        if test.Name not in self.contained_tests:
            self.tests.append(test)
            self.contained_tests.add(test.Name)
            return
        # print(f'Test {test.Name} already in the grid. You cannot have him twice')


@dataclass
class Test:
    Name: str
    groundlvl: float
    Easting: str
    Northing: float
    max_fos_elev: float
    max_ic_elev: float
    min_fos_elev: float
    min_ic_elev: float
    cum_fos: float
    cum_ic: float
    min_fos: float

    def __repr__(self):
        return self.Name



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
            test_item = QStandardItem(test.Name)
            test_attributes = [(k, v) for k, v in test.__dict__.items()]
            self.add_items(test_item, test_attributes)
            self.parent.appendRow(test_item)

    def add_items(self, parent, items):
        for key, value in items:
            parent.appendRow([QStandardItem(str(key)), QStandardItem(str(value))])

