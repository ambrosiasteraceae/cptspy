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
