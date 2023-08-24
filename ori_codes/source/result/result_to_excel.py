import numpy as np
import pandas as pd
"""
result_v1 = np.load("result/result_v1.npy",allow_pickle=True)
result_v1 = pd.DataFrame(result_v1)
result_v1.to_excel("result/result_v1.xlsx")
"""
import pdb
result_v2_all = np.zeros((359,5))
for i in np.arange(5):
    result_v2 = np.load("result/result_v2_{}.npy".format(i),allow_pickle=True)
    for j in np.arange(len(result_v2)):
        result_v2_all[j][i] = result_v2[j]

result_v2_all = pd.DataFrame(result_v2_all)
result_v2_all.to_excel("result/result_v2.xlsx")
