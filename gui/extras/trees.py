from PyQt6.QtWidgets import QTreeView, QTreeWidget, QTreeWidgetItem
import os
class TreeWidgetManager:
    """ A similar lazy loading behaviour but for class instances"""
    _tree_widget_instance = None

    @classmethod
    def get_tree_widget(cls):
        if not cls._tree_widget_instance:
            cls._tree_widget_instance = CustomTreeWidget()

        print(cls._tree_widget_instance.path)
        return cls._tree_widget_instance


class TreeView(QTreeView):
    def __init__(self, parent=None):
        super(TreeView, self).__init__(parent)
        self.tree_widget = TreeWidgetManager.get_tree_widget()
        self.setSelectionMode(QTreeView.SelectionMode.ExtendedSelection)
        self.setModel(self.tree_widget.model())
        self.setRootIndex(self.tree_widget.rootIndex())

    def refresh(self):
        return self.tree_widget.update_tree_view()


class CustomTreeWidget(QTreeWidget):
    def __init__(self):
        super(CustomTreeWidget, self).__init__()
        self.path = None
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1")
        self.setHeaderItem(__qtreewidgetitem)
        self.setObjectName(u"tree")

        self.setColumnCount(2)
        self.setHeaderLabels(['Name', 'Type'])
        self.SelectionMode(True)
        self.doubleClicked.connect(self.print_selection)

    def print_selection(self):
        """
        Opens the file from the tree structure when you double click on it
        """
        # TODO Throws error when you double click on an empty folder
        items = self.selectedItems()
        tree_item = items[0]
        if tree_item.childCount() == 0:
            tree_item_selected = tree_item.text(0)
            parent_item = tree_item.parent().text(0)
            print(tree_item_selected, parent_item, self.path)
            path = os.path.join(self.path, parent_item, tree_item_selected)
            print(path)
            os.system(path)

    def tree_structure_load(self):
        """
        Loads the tree folder structure of the project
        """
        self.clear()
        folders = os.listdir(self.path)

        dirs = {}

        # @TODO add a check if there are other files in the tree structure window
        # Check if it is a directory
        for folder in folders:
            folder_path = os.path.join(self.path, folder)
            if os.path.isdir(folder_path):
                dirs[folder] = os.listdir(folder_path)

        items = []

        for key, values in dirs.items():
            item = QTreeWidgetItem([key])
            for file in values:
                ext = file.split(".")[-1].upper()
                child = QTreeWidgetItem([file, ext])
                item.addChild(child)
            items.append(item)
        self.insertTopLevelItems(0, items)

    def update_tree_view(self):
        """
        Updates the tree view
        """
        self.clear()
        self.tree_structure_load()

