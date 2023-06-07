############################################################

from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import QRect, QCoreApplication, QMetaObject, QAbstractTableModel
from projectinfo import PDWidget

import pandas as pd
import numpy as np
import os
from calc.liquefaction import run_rw1997
from calc.summary import CPTSummary
from overview import on_radio_button_clicked

#@TODO have a console log that tesll you the history of the project or just a console printing whatever is happening
#@TODO When you create a project and you add a few csvs, the nyou calculate and you go back to load tab, and press upload fodler it will uplaod the same
#@TODO when loading a folder and theres no csv, a dialog should appear
#@TODO when loading project requiremetns, and you want to change something you cannot. you need to have an uncheck button to edit? otherwise you have to exit and start again
#@TODO Passing the SCF Parameter
#@TODO Loading a project in the main window and creating the subflder structure shouldnt be allowed. An error shoudl return
#@TODO Run calc should not have the table widget, but the loaded csv files
#@TODO We will need to filter what we save in .npz format. Files are getting big!
#@TODO SAVE ONLY CPT ID as a name in the datafraames not the entirefffp
#TODO: Since cpt objects are loaded into memory everytime you run the program with scf  = 1.3 you multiply the everytime you run it.
class CalcWidget(QWidget):
    def __init__(self, main_window_ref, parent=None):
        super(CalcWidget, self).__init__(parent)
        self.main = main_window_ref
        self.setupUi(self)

    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")

        self.horizontalLayoutWidget_3 = QWidget(Widget)
        self.horizontalLayoutWidget_3.setObjectName(u"horizontalLayoutWidget_3")
        self.horizontalLayoutWidget_3.setGeometry(QRect(20, 40, 1071, 801))
        self.horizontalLayout_4 = QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_4.setSpacing(6)
        self.horizontalLayout_4.setContentsMargins(9, 9, 9, 9)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setSizeConstraint(QLayout.SizeConstraint.SetNoConstraint)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setSpacing(6)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.label_6 = QLabel(self.horizontalLayoutWidget_3)
        self.label_6.setObjectName(u"label_6")

        self.verticalLayout_7.addWidget(self.label_6)

        self.liquefaction_check = QCheckBox(self.horizontalLayoutWidget_3)
        self.liquefaction_check.setObjectName(u"liquefaction_check")

        self.verticalLayout_7.addWidget(self.liquefaction_check)

        self.settlement_check = QCheckBox(self.horizontalLayoutWidget_3)
        self.settlement_check.setObjectName(u"settlement_check")

        self.verticalLayout_7.addWidget(self.settlement_check)

        self.bearing_check = QCheckBox(self.horizontalLayoutWidget_3)
        self.bearing_check.setObjectName(u"bearing_check")

        self.verticalLayout_7.addWidget(self.bearing_check)

        self.commandLinkButton = QCommandLinkButton(self.horizontalLayoutWidget_3)
        self.commandLinkButton.setObjectName(u"commandLinkButton")
        self.commandLinkButton.clicked.connect(self.perform_calc)

        self.verticalLayout_7.addWidget(self.commandLinkButton)

        self.progressBar = QProgressBar(self.horizontalLayoutWidget_3)
        self.progressBar.setObjectName(u"progressBar")
        # self.progressBar.clicked.connet(self.perform_calc)

        self.verticalLayout_7.addWidget(self.progressBar)

        self.pushButton_2 = QPushButton(self.horizontalLayoutWidget_3)
        self.pushButton_2.setObjectName(u"analyses")
        self.pushButton_2.clicked.connect(self.export_to_excel)

        self.verticalLayout_7.addWidget(self.pushButton_2)

        self.pushButton = QPushButton(self.horizontalLayoutWidget_3)
        self.pushButton.setObjectName(u"transferdf")
        self.pushButton.clicked.connect(self.transferdf)

        self.verticalLayout_7.addWidget(self.pushButton)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_7.addItem(self.verticalSpacer_4)

        self.commandLinkButton_2 = QCommandLinkButton(self.horizontalLayoutWidget_3)
        self.commandLinkButton_2.setObjectName(u"commandLinkButton_2")

        self.verticalLayout_7.addWidget(self.commandLinkButton_2)

        self.progressBar_2 = QProgressBar(self.horizontalLayoutWidget_3)
        self.progressBar_2.setObjectName(u"progressBar_2")
        self.progressBar_2.setValue(24)

        self.verticalLayout_7.addWidget(self.progressBar_2)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_7.addItem(self.verticalSpacer_2)

        self.save_figures = QCheckBox(self.horizontalLayoutWidget_3)
        self.save_figures.setObjectName(u"save_figures_check")

        self.verticalLayout_7.addWidget(self.save_figures)

        self.horizontalLayout_4.addLayout(self.verticalLayout_7)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_2)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setSpacing(6)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.label = QLabel(self.horizontalLayoutWidget_3)
        self.label.setObjectName(u"label")

        self.verticalLayout_5.addWidget(self.label)

        self.tableWidget = PDWidget(self.horizontalLayoutWidget_3)
        self.tableWidget.setObjectName(u"tableWidget")

        self.verticalLayout_5.addWidget(self.tableWidget)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_3 = QLabel(self.horizontalLayoutWidget_3)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_2.addWidget(self.label_3)

        self.label_2 = QLabel(self.horizontalLayoutWidget_3)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_2.addWidget(self.label_2)

        self.label_4 = QLabel(self.horizontalLayoutWidget_3)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_2.addWidget(self.label_4)

        self.label_5 = QLabel(self.horizontalLayoutWidget_3)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_2.addWidget(self.label_5)

        self.verticalLayout_5.addLayout(self.horizontalLayout_2)

        self.pushButton_6 = QPushButton(self.horizontalLayoutWidget_3)
        self.pushButton_6.setObjectName(u"pushButton_6")

        self.verticalLayout_5.addWidget(self.pushButton_6)

        self.horizontalLayout_4.addLayout(self.verticalLayout_5)

        self.horizontalLayout_4.setStretch(2, 4588)

        self.retranslateUi(Widget)

        QMetaObject.connectSlotsByName(Widget)

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
        # @TODO When loading a project and you jump straight to perform calc, it breaks

        if not self.commandLinkButton.isEnabled():
            pass

        if self.main.thdf.empty:
            on_radio_button_clicked('No file has been added to compute')
            return

        """Performs the calculations based on the proj_requirements"""

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

        self.fill_table_values(calc_df)

        if self.main.state == 0:
            self.main.tdf.to_excel(self.main.ffp.summary + 'Results.xlsx', index = False)

        self.commandLinkButton.setEnabled(False)





    def export_to_excel(self):
        """Exports the calc_df to excel"""
        self.main.tdf.to_excel(self.main.ffp.summary + 'Results_temp.xlsx')

    def get_table_values(self,active_df):
        """
        Get the overview summary
        """
        # @TODO: Add dialog if you don't have a cumulative fos or ic implimented.
        min_fos = self.main.proj_requirements['cumulative_fos']
        min_ic = self.main.proj_requirements['cumulative_ic']
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
        self.get_table_values(active_df)
        self.label_3.setText(f'CPTs: {self.ncpts}')
        self.label_2.setText(f'Passed: {self.cpts_pass}')
        self.label_4.setText(f'Failed: {self.cpts_fail}')
        self.label_5.setText(f'Percentage Passing: {self.cpts_percentage:.2f}%')

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Widget", None))
        self.label_6.setText(QCoreApplication.translate("Widget", u"Select Analyses", None))
        self.liquefaction_check.setText(QCoreApplication.translate("Widget", u"Liquefaction Triggering", None))
        self.settlement_check.setText(QCoreApplication.translate("Widget", u"Settlement Analysis", None))
        self.bearing_check.setText(QCoreApplication.translate("Widget", u"Bearing Capacity", None))
        self.commandLinkButton.setText(QCoreApplication.translate("Widget", u"Run Calculations", None))
        self.pushButton_2.setText(QCoreApplication.translate("Widget", u"Export to Excel", None))
        self.pushButton.setText(QCoreApplication.translate("Widget", u"TransferDF", None))
        self.commandLinkButton_2.setText(QCoreApplication.translate("Widget", u"Generate Reports", None))
        self.save_figures.setText(QCoreApplication.translate("Widget", u"  Save figures", None))
        self.label.setText(QCoreApplication.translate("Widget", u"Analysis Summary", None))
        self.label_3.setText(QCoreApplication.translate("Widget", u"CPTs", None))
        self.label_2.setText(QCoreApplication.translate("Widget", u"Passed", None))
        self.label_4.setText(QCoreApplication.translate("Widget", u"Failed", None))
        self.label_5.setText(QCoreApplication.translate("Widget", u"Percentage", None))
        self.pushButton_6.setText(QCoreApplication.translate("Widget", u"PushButton", None))

    # retranslateUi

    def calc_load(self):
        #first check to see if the results.xlsx in the summary folder exists
        #if it doesn't

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



# app = QApplication(sys.argv)
#
# # Create the widget window
#
# widget = CalcWidget()
#
# # Show the widget window
# widget.show()
#
# # Start the event loop
# sys.exit(app.exec())
