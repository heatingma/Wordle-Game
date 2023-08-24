import pandas as pd
import numpy as np

wordle_words = pd.read_excel("data_sourse/file/words from wordle.xlsx")
wordle_words = np.array(wordle_words)
np.save("data_sourse/npy/wordle_words.npy",wordle_words)