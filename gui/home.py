import os
import pandas as pd
from PyQt6.QtWidgets import *
from PyQt6.uic import loadUi

from extras import TreeView, GreenMessageBox


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


def define_folder():
    return [
        '/calc',
        '/converted',
        '/figures',
        '/proj_requirements',
        '/raw',
        '/reports',
        '/summary']


class HomeQT(QWidget):
    def __init__(self, main_window_ref):
        super(HomeQT, self).__init__()
        self.main = main_window_ref
        loadUi('uis/home2.ui', self)

        self.folders = define_folder()  # Should be outside the class
        self.treeView.setVisible(False)
        self.load_proj_btn.clicked.connect(self.load_existing_project)
        self.create_proj_btn.clicked.connect(self.create_new_project)

    def create_new_project(self):
        # @TODO Load the treestrucutre in the mainwindow, so it can be used in the other classes
        self.ffp = QFileDialog.getExistingDirectory(self, directory='D:/05_Example')

        if self.ffp:
            for folder in self.folders:
                os.makedirs(self.ffp + folder)

            print(f"Project {self.ffp.split('//')[-1]} created successfully")

            # create the paths for the folders
            paths = create_folder_paths(self.ffp, self.folders)
            # Assign all paths to the main attribute
            self.main.ffp = ProjectPaths(**paths)

            self.treeView.tree_widget.path = self.ffp
            # Load the tree structure
            self.treeView.setVisible(True)
            self.treeView.tree_widget.tree_structure_load()
        return

    def load_dfs(self):
        """
        Loads the dataframes from the summary folder
        """
        if os.path.exists(self.main.ffp.summary + 'Results.xlsx'):
            self.main.df = pd.read_excel(self.main.ffp.summary + 'Results.xlsx')
        if os.path.exists(self.main.ffp.summary + 'Header.xlsx'):
            self.main.hdf = pd.read_excel(self.main.ffp.summary + 'Header.xlsx')

    def load_existing_project(self):
        # @TODO Exists the GUI if you cancel the command. This is everywhere
        # @TODO ADD a reload button in case you put items in the folder to update the tree view?

        self.ffp = QFileDialog.getExistingDirectory(self, directory='D:/05_Example')

        if self.ffp:
            paths = create_folder_paths(self.ffp, self.folders)
            self.main.ffp = ProjectPaths(**paths)
            self.load_case_manager()

            #
            # self.treeView.tree_widget.path = self.ffp
            # self.treeView.tree_widget.tree_structure_load()
            # self.main.convert.update_list_view()
            #
            # print(f"Successfully loaded {self.ffp.split('/')[-1]}  project")
            # self.treeView.setVisible(True)
            # # if len(os.listdir(self.main.ffp.summary)) > 1:
            # self.load_dfs()
            #
            # self.main.loadcsv.upload_folder()
            # self.main.loadcsv.load_cpts()
            # self.main.proj_req.load_proj_requirements()

        return

    def load_header(self):
        #Load header
        self.main.hdf = pd.read_excel(self.main.ffp.summary + 'Header.xlsx')

    def load_results(self):
        #Load results
        self.main.df = pd.read_excel(self.main.ffp.summary + 'Results.xlsx')

    def load_tree(self):
        self.treeView.tree_widget.path = self.ffp
        self.treeView.tree_widget.tree_structure_load()
        self.treeView.setVisible(True)

    def load_case_manager(self):
        # 1 summary is empty
        # 1.1 Check in the raw files.
        #   1.1.1 -> check if pending raw files
        #       1.1.1.1 -> No pending raw files
        #       1.1.1.2 -> Pending raw files

        # 2 summary is full
        #   2.1 differences in sizes? (via ID) check
        #       yes
        #       2.1.1 -> Message Box (You have remaining files to convert. Would you like to process them now?)
        #       2.1.2 -> Proess them
        #        No
        #          2.1.3 -> Message Box (Success)
        # 3 summary only contains header
        #   3.1 -> You have remaining files to calculate. Would you like to add more or convert them?

        #   4 summary only contains results

        case = self.check_summary()
        cases = {
            1: self.load_case_1,
            2: self.load_case_2,
            3: self.load_case_3,
            # 4: self.load_case_4,
        }

        return cases[case]()


    def check_summary(self):
        summary_files = os.listdir(self.main.ffp.summary)

        if not summary_files:
            return 1
        if 'Results.xlsx' in summary_files and 'Header.xlsx' in summary_files:
            return 2
        elif 'Header.xlsx' in summary_files and not 'Results.xlsx' in summary_files:
            return 3
        else:
            return 4

    def load_case_1(self):
        """
        See load case manager docstrings.
        """
        self.load_tree()
        self.main.proj_req.load_proj_requirements()

        raw_files = os.listdir(self.main.ffp.raw)
        converted_files = os.listdir(self.main.ffp.converted)

        if converted_files:
            # self.main.loadcsv.upload_folder_new_proj()
            GreenMessageBox(f'Project {os.path.basename(self.ffp)} loaded succesfully. \n'
                            f'Converted files are pending to be processed.')
        else:
            if raw_files:
                self.main.convert.update_list_view()
                GreenMessageBox(f'Project {os.path.basename(self.ffp)} loaded succesfully. \n'
                                f'Raw files are pending to be converted.')
            else:
                GreenMessageBox(f'Project {os.path.basename(self.ffp)} loaded succesfully. \n'
                                f'No pending files.')

        # print(f"Successfully loaded {self.ffp.split('/')[-1]}  project")


    def load_case_2(self):
        """
        See load case manager docstrings.
        """

        self.load_header()
        self.load_results()

        header_cpts = set(self.main.hdf['CPT-ID'].unique())
        results_cpts = set(self.main.df['CPT-ID'].unique())

        diff1 = header_cpts - results_cpts
        #get the
        directory_files = set([fname.split('.')[0] for fname in os.listdir(self.main.ffp.converted)])
        diff2 = directory_files - results_cpts
        difference = diff1.union(diff2)

        # difference = header_cpts - results_cpts
        print(difference)
        if len(difference) == 0:
            GreenMessageBox(f'Project {os.path.basename(self.ffp)} loaded succesfully. \n'
                            f'No pending files.')
        else:
            GreenMessageBox(f'Project {os.path.basename(self.ffp)} loaded succesfully. \n'
                            f'There are {len(difference)} CPTs not yet processed.')
            #we have some cpts not in the results
            remaining = [self.main.ffp.converted + cpt + '.csv' for cpt in difference]
            # self.main.loadcsv.process_files(remaining)
            #Put a condition for the proess_files to not create a new header.xlsx

        self.load_tree()
        self.main.proj_req.load_proj_requirements()
        return

    def load_case_3(self):

        self.load_header()
        GreenMessageBox(f'Project {os.path.basename(self.ffp)} loaded succesfully. \n'
                        f'There are  {len(os.listdir(self.main.ffp.converted))} pending for processing.')

        self.main.loadcsv.upload_folder_new_proj()
        self.load_tree()
        self.main.proj_req.load_proj_requirements()







