import pandas as pd

from PyQt6.QtWidgets import *
from PyQt6.uic import loadUi

from extras import PDWidget, TreeView, GreenMessageBox, RedMessageBox


def on_radio_button_clicked(msg):
    # message_box = QMessageBox()
    # message_box.setWindowTitle("Information")
    # message_box.setText(f"{msg}")
    # message_box.exec()
    RedMessageBox(msg)


class OverviewQT(QWidget):
    def __init__(self, main_window_ref):
        self.main = main_window_ref
        super(OverviewQT, self).__init__()

        loadUi('uis/overview2.ui', self)

        self.merge_dfs.clicked.connect(self.merge_dataframes)
        self.sort_dfs.clicked.connect(self.sort_and_arrange)
        self.save_dfs.clicked.connect(self.save_dataframes)

        self.radioButton_1.clicked.connect(self.view_temp_header)
        self.radioButton_2.clicked.connect(self.view_temp_results)
        self.radioButton_3.clicked.connect(self.view_main_header)
        self.radioButton_4.clicked.connect(self.view_main_results)

        self.previous_btn.clicked.connect(self.main.tab_widget.previous)
        self.next_btn.clicked.connect(self.main.tab_widget.next)

    def view_main_header(self):
        if not self.main.hdf.empty:
            self.table.loadDF('123', self.main.hdf)
            # print(self.main.hdf.head())
            # self.main.something.tableWidget.loadDF('123', self.main.hdf)
            return
        on_radio_button_clicked('No Project Header was Added nor Created')
        # self.radioButton_3.setChecked(False)
        # self.get_current_radio_check()

    def view_main_results(self):
        if not self.main.df.empty:
            self.table.loadDF('123', self.main.df)
            return
        on_radio_button_clicked('No Project Calc was Added nor Created')
        # self.radioButton_4.setChecked(False)
        # self.get_current_radio_check()

    def view_temp_header(self):
        if not self.main.thdf.empty:
            self.table.loadDF('123', self.main.thdf)
            return
        on_radio_button_clicked('No Newly files were Added nor Created')
        self.table.loadDF('123', self.main.thdf)
        # self.radioButton_1.setChecked(False)
        # self.get_current_radio_check()

    def view_temp_results(self):
        if not self.main.tdf.empty:
            self.table.loadDF('123', self.main.tdf)
            return
        on_radio_button_clicked('No Newly files were Added nor Created - Calc')
        # self.radioButton_2.setChecked(False)
        # self.get_current_radio_check()

    def get_current_radio_check(self):
        radios = self.findChildren(QRadioButton)
        for radio in radios:
            if radio.isChecked():
                return radio.setChecked(True)

    def merge_dataframes(self):

        if self.main.tdf.empty or self.main.thdf.empty:
            on_radio_button_clicked(
                f"{'No new files have been loaded' if self.main.thdf.empty else 'Results have not been computed'}")
            return

        self.main.df = pd.concat([self.main.df, self.main.tdf], ignore_index=True)
        self.main.hdf = pd.concat([self.main.hdf, self.main.thdf], ignore_index=True)

        # # Check differences in header
        # mask_dif = self.main.thdf['Name'].isin(self.main.hdf['Name'])
        # if mask_dif.any():
        #     self.main.hdf = pd.concat((self.main.hdf, self.main.thdf[~mask_dif])).reset_index(drop=True)

        # save to excel
        self.main.df.to_excel(self.main.ffp.summary + 'Results.xlsx', index=False)
        self.main.hdf.to_excel(self.main.ffp.summary + 'Header.xlsx', index=False)
        self.merge_dfs.setEnabled(False)

        self.main.thdf = pd.DataFrame()
        self.main.tdf = pd.DataFrame()



        GreenMessageBox('Current session tests have been succesfully merged with the project tables')
        return

    def sort_and_arrange(self):
        # Maybe sort and arrange
        #Throws error if you sort or arrange empty dataframe
        if self.main.df.empty and self.main.hdf.empty:
            return
        self.main.df.dropna(inplace=True, how='all')
        self.main.df.dropna(subset=['Northing', 'Easting'], inplace=True)
        self.main.hdf.dropna(inplace=True, how='all')
        self.main.hdf.dropna(subset=['Northing', 'Easting'], inplace=True)
        self.main.hdf.drop_duplicates(inplace=True, subset=['Name'])
        self.main.df.drop_duplicates(inplace=True, subset=['Name'])
        self.main.hdf.sort_values(by=['Name'], inplace=True)
        self.main.df.sort_values(by=['Name'], inplace=True)
        self.table.updateView(self.main.df)

    def save_dataframes(self):
        print('savebtn pressedf')
        self.main.df.to_excel(self.main.ffp.summary + 'Results.xlsx', index=False)
        self.main.hdf.to_excel(self.main.ffp.summary + 'Header.xlsx', index=False)
        GreenMessageBox("Succesfully saved both dataframes")


