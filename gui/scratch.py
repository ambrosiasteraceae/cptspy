import pandas as pd
import glob
from calc.liquefaction import run_rw1997
from calc.summary import CPTSummary
from load.loading import load_dataframe, load_mpa_cpt_file
from miscellaneous.timed import timed
from tqdm import tqdm

ffps = glob.glob('D:/04_R&D/cptspy/output/' + '*.csv')
df = load_dataframe(ffps)

summary_df = df[['CPT-ID', 'groundlvl','Easting', 'Northing']]

@timed
def generate_df():
    data = []
    for j in range(len(df)):
        cpt = df['Object'][j]
        rw = run_rw1997(cpt, pga=0.12, m_w=6, gwl=2)
        cpt_summary = CPTSummary(rw).__dict__
        data.append(list(cpt_summary.values()))
    newdf = pd.DataFrame(data, columns=cpt_summary.keys())
    return newdf



summary = generate_df()
print(summary.head())


concatdf = pd.concat([summary_df, summary], axis=1)




# @timed
# def run():
#     for j in range(10):
#         for i in tqdm(range(len(df))):
#             cpt = df['Object'][i]
#             rw=run_rw1997(cpt, pga = 0.12, m_w = 6, gwl = 2)
#             CPTSummary(rw)


def upload_file(self):
    file_name, _ = QFileDialog.getOpenFileName(self, 'Open file', '', "CSV (*.csv)")
    if file_name:
        if file_name not in self.uploaded_files:
            self.uploaded_files.add(file_name)
            self.model.appendRow(QStandardItem(file_name))
        else:
            QMessageBox.warning(self, "Duplicate File", "This file has already been uploaded.")
    else:
        return



def upload_folder(self):
    folder_path = QFileDialog.getExistingDirectory(self, "Open Folder")
    if folder_path:
        folder_files = [
            os.path.join(folder_path, file_name) for file_name in os.listdir(folder_path) if file_name.endswith(".csv")
        ]
        new_files = set(folder_files) - self.uploaded_files
        if new_files:
            self.uploaded_files.update(new_files)
            self.model.appendRows([QStandardItem(file_name) for file_name in new_files])
        else:
            QMessageBox.information(self, "No New Files", "There are no new CSV files in the selected folder.")
    else:
        return


def load_cpts(self):
    ffps = [self.model.item(i).text() for i in range(self.model.rowCount())]

    if not ffps:
        QMessageBox.warning(self, "No Files", "Please upload CSV files before loading CPTs.")
        return