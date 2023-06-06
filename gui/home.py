from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import QRect, QCoreApplication, QMetaObject, QAbstractTableModel, Qt
import os
import pandas as pd
#@TODO Set number to the tree widget to se the number of files.
#@TODO Also if possible have the tree widget show only 10 items if there are a lot of elements


class TreeWidgetManager:
    """ A similar lazy loading behaviour but for class instances"""
    _tree_widget_instance = None

    @classmethod
    def get_tree_widget(cls):
        if not cls._tree_widget_instance:
            print('initial call')
            cls._tree_widget_instance = CustomTreeWidget()
        print('second call')
        print(cls._tree_widget_instance.path)
        return cls._tree_widget_instance



class TreeView(QTreeView):
    def __init__(self):
        super(TreeView, self).__init__()
        self.tree_widget = TreeWidgetManager.get_tree_widget()
        self.setSelectionMode(QTreeView.SelectionMode.ExtendedSelection)
        self.setModel(self.tree_widget.model())
        self.setRootIndex(self.tree_widget.rootIndex())

    def refresh(self):
        return self.tree_widget.update_tree_view()



class CustomTreeWidget(QTreeWidget):
    def __init__(self):
        super(CustomTreeWidget,self).__init__()
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
        #TODO Throws error when you double click on an empty folder
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

        print('Path is:', self.path)
        # for folder in folders:
        #     dirs[folder] = os.listdir(os.path.join(self.path, folder))

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

    # def update_tree_view(self):
    #     """
    #     Updates the tree view
    #     """
    #     self.clear()
    #     self.tree_structure_load()


class ProjectPaths:
    """Stores the project paths for all the sub folders"""

    def __init__(self, proj, calc, converted, figures, proj_requirements, raw, reports, summary):
        self.proj = proj
        self.calc = calc
        self.converted = converted
        self.figures = figures
        self.proj_requirements = proj_requirements
        self.raw = raw
        self.reports = reports
        self.summary = summary


def create_folder_paths(main_path, folder_list):
    paths = {}
    for folder in folder_list:
        paths[folder.strip('/')] = main_path + folder + '/'
    paths['proj'] = main_path

    return paths


class HomeQT(QWidget):
    def __init__(self, main_window_ref):
        super(HomeQT, self).__init__()
        self.main = main_window_ref
        self.setupUi(self)

    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")

        self.verticalLayoutWidget = QWidget(Widget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        # Set layout widget in the center

        self.verticalLayoutWidget.setGeometry(QRect(0, 10, 261, 581))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.pushButton_2 = QPushButton(self.verticalLayoutWidget)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.verticalLayout.addWidget(self.pushButton_2)

        self.pushButton = QPushButton(self.verticalLayoutWidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.clicked.connect(self.load_existing_project)

        self.verticalLayout.addWidget(self.pushButton)

        # self.tree = QTreeWidget(self.verticalLayoutWidget)
        # __qtreewidgetitem = QTreeWidgetItem()
        # __qtreewidgetitem.setText(0, u"1");
        # self.tree.setHeaderItem(__qtreewidgetitem)
        # self.tree.setObjectName(u"tree")
        # self.tree.setColumnCount(2)
        # self.tree.setHeaderLabels(['Name', 'Type'])
        # self.tree.SelectionMode(True)
        # self.tree.doubleClicked.connect(self.print_selection)

        # self.tree = CustomTreeWidget()
        self.tree = TreeWidgetManager().get_tree_widget()
        # print(self.tree)
        self.verticalLayout.addWidget(self.tree)

        self.retranslateUi(Widget)

        QMetaObject.connectSlotsByName(Widget)

        self.folders = self.define_folder()

        self.pushButton_2.clicked.connect(self.create_new_project)
        # self.pushButton_2.clicked.connect(self.tree.update_tree_view)


    def retranslateUi(self, Widget):

        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Widget", None))
        self.pushButton_2.setText(QCoreApplication.translate("Widget", u"Create a new project", None))
        self.pushButton.setText(QCoreApplication.translate("Widget", u"Load a new project", None))

    def print_selection(self):
        """
        Opens the file from the tree structure when you double click on it
        """
        # TODO Throws error when you double click on an empty folder
        items = self.tree.selectedItems()
        tree_item = items[0]
        if tree_item.childCount() == 0:
            tree_item_selected = tree_item.text(0)
            parent_item = tree_item.parent().text(0)
            print(tree_item_selected, parent_item, self.ffp)
            path = os.path.join(self.ffp, parent_item, tree_item_selected)
            print(path)
            os.system(path)


    def tree_structure_load(self):
        """
        Loads the tree folder structure of the project
        """
        self.tree.clear()
        folders = os.listdir(self.ffp)

        dirs = {}

        for folder in folders:
            dirs[folder] = os.listdir(os.path.join(self.ffp, folder))

        #@TODO add a check if there are other files in the tree structure window
        # Check if it is a directory
        # for folder in folders:
            # folder_path = os.path.join(self.ffp, folder)
            # if os.path.isdir(folder_path):
            #     dirs[folder] = os.listdir(folder_path)
        items = []

        for key, values in dirs.items():
            item = QTreeWidgetItem([key])
            for file in values:
                ext = file.split(".")[-1].upper()
                child = QTreeWidgetItem([file, ext])
                item.addChild(child)
            items.append(item)
        self.tree.insertTopLevelItems(0, items)

    @staticmethod
    def define_folder():
        return [
            '/calc',
            '/converted',
            '/figures',
            '/proj_requirements',
            '/raw',
            '/reports',
            '/summary']


    def create_new_project(self):
        # @TODO Load the treestrucutre in the mainwindow, so it can be used in the other classes
        self.ffp = QFileDialog.getExistingDirectory(self, directory='D:/05_Example')
        # self.main.pfp = self.ffp
        for folder in self.folders:
            os.makedirs(self.ffp + folder)
        print(f"Project {self.ffp.split('//')[-1]} created succesfuly")

        # create the paths for the folders
        paths = create_folder_paths(self.ffp, self.folders)
        # Assign all paths to the main attribute
        self.main.ffp = ProjectPaths(**paths)
        # Load the tree structure
        self.tree_structure_load()



    def load_dfs(self):
        """
        Loads the dataframes from the summary folder
        """
        if os.listdir(self.main.ffp.summary):
            self.main.df = pd.read_excel(self.main.ffp.summary + 'Results.xlsx')
            self.main.hdf = pd.read_excel(self.main.ffp.summary + 'Header.xlsx')




    def load_existing_project(self):
        #@TODO Exists the GUI if you cancel the command. This is everywhere
        #@TODO ADD a reload button in case you put items in the folder to update the tree view?


        self.main.state = 1
        self.ffp = QFileDialog.getExistingDirectory(self, directory='D:/05_Example')


        paths = create_folder_paths(self.ffp, self.folders)
        self.main.ffp = ProjectPaths(**paths)

        self.tree.path = self.ffp
        self.tree.tree_structure_load()
        print('MY tree is now gone: ', self.tree)

        #We need to initialize the list_view in the convert tab
        #@TODO Maybe a dialog box saying that pending items have been found.Would you like to convert them?
        self.main.convert.update_list_view()


        # self.tree_structure_load()
        print(f"Successfully loaded {self.ffp.split('/')[-1]}  project")

        if os.listdir(self.main.ffp.summary):
            self.load_dfs()
            self.main.loadcsv.upload_folder()
            self.main.loadcsv.load_cpts()
            self.main.proj_req.load_proj_requirements()




        # self.main.overview.view_main_header()

        # self.main.overview.load_df()




# import sys
# app = QApplication(sys.argv)
#
# # Create the widget window
#
# widget = HomeQT(123)
#
# # Show the widget window
# widget.show()
#
# # Start the event loop
# sys.exit(app.exec())
