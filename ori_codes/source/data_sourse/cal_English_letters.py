import numpy as np
import pandas as pd
words = np.load("data_sourse/words.npy",allow_pickle=True)
letter_num = np.zeros(26)
for i in np.arange(len(words)):
    word = words[i][0]
    for j in np.arange(5):
        letter_num[ord(word[j])-97] += 1

for i in np.arange(26):
    letter_num[i] /= (len(words)*5)
        
np.save("data_sourse\letter_num.npy",letter_num)
letter_num = pd.DataFrame(letter_num)
letter_num.to_excel("data_sourse/file/letter_num.xlsx")