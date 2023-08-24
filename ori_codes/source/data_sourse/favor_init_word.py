import pandas as pd
import numpy as np

favor = pd.read_excel("data_sourse/file\possible_favor_init_word.xlsx")
np.save("data_sourse/favor_init_word.npy",favor)