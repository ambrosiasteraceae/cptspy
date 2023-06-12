import pandas as pd
import numpy as np
import os

from PyQt6.QtWidgets import *
from PyQt6.uic import loadUi

from extras import PDWidget, GreenMessageBox, RedMessageBox
from calc.liquefaction import run_rw1997
from calc.summary import CPTSummary
from overview import on_radio_button_clicked


class CalcWidget(QDialog):
    def __init__(self, main_window_ref, parent=None):
        super(CalcWidget, self).__init__(parent)

        loadUi('uis/calculations2.ui', self)
        self.main = main_window_ref

        self.extra_btn.clicked.connect(self.transferdf)
        self.export_excel_btn.clicked.connect(self.export_to_excel)
        self.run_calc_cmd.clicked.connect(self.perform_calc)

        self.previous_btn.clicked.connect(self.main.tab_widget.previous)
        self.next_btn.clicked.connect(self.main.tab_widget.next)


    def transferdf(self):
        # print(self.main.df.head())
        self.tableWidget.loadDF('aa', self.main.df)
        pass

    def check_states(self):
        """Checks the states of the checkboxes and updates the proj_requirements in the main class"""
        checks = self.findChildren(QCheckBox)
        for check in checks:
            self.main.proj_requirements[check.objectName()] = check.isChecked()
        print(self.main.proj_requirements)

        # print(self.main.proj_requirements)

    def perform_calc(self):
        """Performs the calculations based on the proj_requirements"""

        if not self.run_calc_cmd.isEnabled():  # We enable it only once
            pass

        if self.main.thdf.empty:
            on_radio_button_clicked('No file has been added to compute')
            return

        m_w = self.main.proj_requirements['m_w']
        pga = self.main.proj_requirements['pga']
        gwl = self.main.proj_requirements['gwl']
        scf = self.main.proj_requirements['scf']
        print(f'SCF IS {scf}')

        # print(type(m_w), type(pga), type(gwl), type(scf))
        # cumulative_ic = self.main.proj_requirements['cumulative_ic']
        # cumulative_fos = self.main.proj_requirements['cumulative_fos']
        # liquefaction_check = self.main.proj_requirements['liquefaction_check']
        # settlement_check = self.main.proj_requirements['settlement_check']
        # bearing_check = self.main.proj_requirements['bearing_check']
        # save_figures = self.main.proj_requirements['save_figures']

        data = []
        # print(self.main.df.head())
        # ffp_npz = 'D:/04_R&D/cptspy/gui/project/calc/'
        for i, cpt in enumerate(self.main.thdf['Object']):
            cpt.q_c = cpt.q_c * scf  # Add SCF

            rw1997 = run_rw1997(cpt, gwl=gwl, pga=pga, m_w=m_w)

            summary = CPTSummary(rw1997)
            array_dict = {**cpt.__dict__, **rw1997.__dict__}

            np.savez(self.main.ffp.calc + cpt.file_name, **array_dict)

            data.append(list(summary.__dict__.values()))

            self.progressBar.setValue(int(i / len(self.main.thdf) * 100))

        calc_df = pd.DataFrame(data, columns=list(summary.__dict__.keys()))

        main_df = self.main.thdf[['CPT-ID', 'groundlvl', 'Easting', 'Northing']]

        self.main.tdf = pd.concat([main_df, calc_df], axis=1)
        self.tableWidget.loadDF('aa', self.main.tdf)
        self.progressBar.setValue(100)

        try:
            self.fill_table_values(calc_df)
        except TypeError:
            RedMessageBox('Cumulative soil type index Ic or liquefaction FoS criteria have not been defined')
            return
        GreenMessageBox(f"Calculations finished for {self.main.thdf['Object'].size}.")

        # if self.main.state == 0:
        # if not os.path.exists(self.main.ffp.summary + 'Results.xlsx'):
        #     self.main.tdf.to_excel(self.main.ffp.summary + 'Results.xlsx', index=False)

        self.run_calc_cmd.setEnabled(False)

    def export_to_excel(self):
        """Exports the calc_df to excel"""
        self.main.tdf.to_excel(self.main.ffp.summary + 'Results_temp.xlsx')

    def get_table_values(self, active_df):
        """
        Get the overview summary
        """
        # @TODO: Add dialog if you don't have a cumulative fos or ic implimented.

        min_fos = self.main.proj_requirements['cumulative_fos']
        min_ic = self.main.proj_requirements['cumulative_ic']
        if min_fos is None and min_ic is None:
            raise ValueError('Cumulative soil type index Ic or liquefaction FoS criteria have not been defined')

        self.ncpts = active_df.shape[0]
        a = active_df['cum_fos'] > min_fos
        b = active_df['cum_ic'] > min_ic
        # print('Min fos:',a,type(a))
        # print('Min ic:',b,type(b))

        s_mask = (active_df['cum_fos'] > min_fos) | (active_df['cum_ic'] > min_ic)
        self.cpts_fail = active_df['cum_fos'][s_mask].shape[0]
        self.cpts_pass = self.ncpts - self.cpts_fail
        self.cpts_percentage = self.cpts_pass / self.ncpts * 100

    def fill_table_values(self, active_df):
        """Fills the table with the values from the calc_df"""
        try:
            self.get_table_values(active_df)
        except ValueError as e:
            return e
        self.ncpts_label.setText(f'CPTs: {self.ncpts}')
        self.cpts_pass_label.setText(f'Passed: {self.cpts_pass}')
        self.cpts_fail_label.setText(f'Failed: {self.cpts_fail}')
        self.cpts_percentage_label.setText(f'Percentage Passing: {self.cpts_percentage:.2f}%')


    def calc_load(self):
        # first check to see if the results.xlsx in the summary folder exists
        # if it doesn't
        filepath = self.main.ffp.summary + 'Results.xlsx'
        if os.path.exists(filepath):
            self.handle_loaded_proj()
            return
        else:
            self.perform_calc()

    def handle_loaded_proj(self):
        pass

    def handle_loaded_proj(self):
        already_processed = set(self.main.hdf['ffp'])
