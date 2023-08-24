import numpy as np
import matplotlib.pyplot as plt
fre = np.load("fre.npy")
X = np.arange(243)
plt.bar(x=X,height=fre)
plt.show()