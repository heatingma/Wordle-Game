import numpy as np
import pandas as pd
import pdb
import matplotlib.pyplot as plt

ratio = pd.read_excel("result/result_v1_ratio.xlsx")
ratio = pd.read_excel("result/result_v1_ratio2.xlsx")
ratio = np.squeeze(np.array(ratio))
ratio_count = []
begin = ratio[0]
count = 1
for i in np.arange(len(ratio)-1):
    if(ratio[i+1]!=begin):
        ratio_count.append([100*begin,count])
        count = 1
        begin = ratio[i+1]
    else:
        count += 1

ratio_count.append([100*begin,count])
ratio_count = np.array(ratio_count)
plt.figure()
plt.title("ratio")
plt.xlabel("ratio")
plt.ylabel("number")
plt.bar(x=ratio_count[:,0],height=ratio_count[:,1],width=0.5)
plt.savefig("result/ratio.png")
ratio_count = pd.DataFrame(ratio_count)
#ratio_count.to_excel("result/ratio_process.xlsx")

    