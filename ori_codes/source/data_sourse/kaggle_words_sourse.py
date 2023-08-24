import numpy as np
import pandas as pd

kaggle_words = pd.read_excel("data_sourse/frequency from kaggle.xlsx")
np.save("data_sourse/kaggle_words.npy",kaggle_words)

