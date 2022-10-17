import liquepy as lq
import matplotlib.pyplot as plt


cpt = lq.field.load_mpa_cpt_file("output/CPT_N21d.csv", delimiter=";")
#bf, sps = plt.subplots(ncols=3, sharey=True, figsize=(8, 6))

print(cpt.file_name)



bi2014 = lq.trigger.run_bi2014(cpt, pga=0.25, m_w=7.5, gwl=2.5)

# print(bi2014.s_g)
# print(bi2014.saturation)
# print(bi2014.gwl)
# print(bi2014.unit_wt)
print(bi2014.s_g_water)

bf, sps = plt.subplots(ncols=4, sharey=True, figsize=(8, 6))
lq.fig.make_bi2014_outputs_plot(sps, bi2014)
plt.show()


print(bi2014.factor_of_safety[bi2014.factor_of_safety <1.25].size)
