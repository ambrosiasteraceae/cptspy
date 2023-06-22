import shutil

from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.uic import loadUi
from read.reading import *
from extras import TreeView, RedMessageBox, GreenMessageBox


def escape(string):
    extensions = ['PO', 'PRE']
    for ext in extensions:
        if ext in string:
            return ext + string.split(ext)[1].split('.')[0]
    return string.split('.')[0]


class ConvertQT(QWidget):
    def __init__(self, main_window_ref):
        super(ConvertQT, self).__init__()
        self.main = main_window_ref
        loadUi('uis/convert2.ui', self)

        self.progressBar.setValue(0)
        self.model_log = QStandardItemModel(self.list_view_log)
        self.model_convert = QStandardItemModel(self.list_view_convert)
        self.convert.clicked.connect(self.convert_files)
        self.list_view_convert.setModel(self.model_convert)
        self.list_view_log.setModel(self.model_log)
        self.load_folder_btn.clicked.connect(self.upload_folder)
        self.uploaded_files = set()

        self.previous_btn.clicked.connect(self.main.tab_widget.previous)
        self.next_btn.clicked.connect(self.main.tab_widget.next)
        self.refresh_btn.clicked.connect(self.treeView.refresh)


    def get_all_pass_and_fail_files(self):
        dirs = ['pass/', 'fail/']
        processed = set()

        for directory in dirs:
            ffp = os.path.join(self.main.ffp.raw, directory)


            if not os.path.exists(ffp):
                return processed

            _files = glob.glob(ffp + '*.xlsx')
            _files = [os.path.basename(f) for f in _files]
            processed.update(set(_files))

        return processed


    def upload_folder(self):

        folder_name = QFileDialog.getExistingDirectory(self, 'Open Folder', directory='D:/01_Projects/38.Al Hudayriyat')
        patterns = ['/*.xlsx', '/*.xls']
        folder_files = []
        for pattern in patterns:
            folder_files.extend(glob.glob(folder_name +  pattern))
        # folder_files = glob.glob(folder_name + '/*.xlsx')

        self.processed = self.get_all_pass_and_fail_files()
        _files_to_copy = [os.path.basename(f) for f in folder_files]

        _files_to_copy = set(_files_to_copy) - self.processed #files_to_copy now only holds the path_basename


        files_to_copy = [os.path.join(folder_name, f) for f in _files_to_copy]

        print('so far so good')
        if files_to_copy:
            GreenMessageBox('iles To COpy')
            self.progressBar.setValue(0)
            self.move_files_to_directory(files_to_copy)
            self.update_list_view()
        elif not folder_files:
            RedMessageBox('No .xlsx or .xls files in the folder')
            # RedMessageBox('No .xlsx files in the folder')
        else:
            # RedMessageBox.warning(self, 'Warning', 'You are trying to insert files that have already been uploaded')
            RedMessageBox('You are trying to insert files that have already been uploaded')


    def move_files_to_directory(self, file_list):
        for f in file_list:
            shutil.copy(f, self.main.ffp.raw)

    def update_list_view(self):
        # The idea is to list the files that are yet to be converted. Sitting outside the fail/pass fodlers
        files_to_add = glob.glob(self.main.ffp.raw + "*.xlsx")
        files_to_add.extend(glob.glob(self.main.ffp.raw + "*.xls"))
        if files_to_add:
            print(f"{len(files_to_add)} being updated")
            new_files = set(files_to_add) - self.uploaded_files

            if new_files:
                self.uploaded_files.update(new_files)
                for file_name in new_files:
                    self.model_convert.appendRow(QStandardItem(os.path.basename(file_name)))
        self.loaded_files_label.setText(f"{len(files_to_add)} raw files loaded")
        self.treeView.refresh()


    def convert_files(self):

        passed_path = os.path.join(self.main.ffp.raw, 'pass/')
        failed_path = os.path.join(self.main.ffp.raw, 'fail/')

        self.pass_nr = 0
        self.fail_nr = 0

        if not os.path.exists(passed_path):
            os.makedirs(passed_path)
        if not os.path.exists(failed_path):
            os.makedirs(failed_path)

        for i, file in enumerate(self.uploaded_files):
            self.convert_file_gui(file, passed_path, failed_path)

            percentage = int(i/len(self.uploaded_files)* 100)
            if percentage % 5 == 0:
                self.progressBar.setValue(percentage)


        self.uploaded_files = set()
        self.progressBar.setValue(100)

        self.update_list_view()
        self.model_convert.clear()

        self.label_converted.setText(f"Converted: {self.pass_nr} files")
        self.label_failed.setText(f"Failed: {self.fail_nr} files")
        GreenMessageBox(f'Convert procedure finished.\n '
                        f'{self.pass_nr} files were converted \n'
                        f'{self.fail_nr} files failed to convert')



    def convert_file_gui(self, ffp, ffp_passed, ffp_fail):

        fns = [convert_nmdc_to_csv_00, convert_nmdc_to_csv_01, convert_cs_to_csv_01, convert_cs_to_csv_02]
        for i, fn in enumerate(fns):
            res = fn(ffp)
            file_name = os.path.basename(ffp)
            file_name_shortcut = escape(file_name)
            if isinstance(res, pd.DataFrame):
                # We found the right converter
                res.to_csv(self.main.ffp.converted + f"{file_name.split('.')[0]}.csv", index=False, sep=';')
                os.rename(ffp, os.path.join(ffp_passed, file_name))
                self.model_log.appendRow(QStandardItem(f"{file_name_shortcut} loaded successfully."))
                self.pass_nr +=1
                return

            if i == len(fns) - 1:
                # We reached the end of the list and no converter was found
                os.rename(ffp, os.path.join(ffp_fail, file_name))
                self.model_log.appendRow(QStandardItem(f"{file_name_shortcut} failed to load."))
                self.fail_nr +=1

    def upload_file(self):
        pass
