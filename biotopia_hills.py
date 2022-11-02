from loading import loading
from read import reading


fp_in = "C:/Users/dgs/OneDrive/04_R&D/cptspy/biotopia/input"
fp_out = "C:/Users/dgs/OneDrive/04_R&D/cptspy/biotopia/output"


reading.convert_file(fp_in, fp_out, verbose = True)

print(loading.load_dataframe(fp_out))