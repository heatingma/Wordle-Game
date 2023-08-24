import numpy as np
import matplotlib.pyplot as plt
X = np.array([1,2,3,4,5,6,7])
Y = np.array([0,0,16.6,61.4,21.7,0.3,0])
plt.bar(x=X,height=Y,width=0.8,color=['violet','blueviolet','darkorchid','indigo','blueviolet','mediumorchid','violet',])
plt.xlabel("tries number")
plt.ylabel("ratio")
plt.title("Prediction of EERIE")
plt.savefig("result/ori_result_v_102_EERIE.png")