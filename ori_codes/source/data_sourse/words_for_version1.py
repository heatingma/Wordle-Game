import numpy as np
words = np.load('data_sourse\words.npy',allow_pickle=True)
words_for_version1 = []
for i in np.arange(len(words)):
    words_for_version1.append([words[i][0],words[i][3],'True'])
np.save('data_sourse\words_for_version1.npy',words_for_version1)
