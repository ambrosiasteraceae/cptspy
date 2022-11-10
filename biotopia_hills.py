from loading import loading
from read import reading
import liquepy as lq
from calc.liquefaction import  run_rw1997
import matplotlib.pyplot as plt
fp_in = "C:/Users/dgs/OneDrive/04_R&D/cptspy/biotopia/input"
fp_out = "C:/Users/dgs/OneDrive/04_R&D/cptspy/biotopia/output/"


#reading.convert_file(fp_in, fp_out, verbose = True)

dfs = loading.load_dataframe(fp_out)
print(dfs)

for i, cpt in enumerate(dfs['Object'][0:1]):
    rw1997 = lq.trigger.run_bi2014(cpt, pga=0.122, m_w=0.6, gwl=2)
    #bi2014 = lq.trigger.run_bi2014(cpt, pga=0.122, m_w=0.6, gwl=2)
    print(rw1997.cpt.q_c[0:10])

    # plt.plot(rw1997.factor_of_safety, -rw1997.depth, c = 'r')
    # plt.plot(bi2014.factor_of_safety, -rw1997.depth, c='b')
    # plt.show()