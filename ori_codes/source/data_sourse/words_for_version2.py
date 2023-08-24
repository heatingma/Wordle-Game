import numpy as np
words = np.load('data_sourse/npy/words.npy',allow_pickle=True)
words_for_version2 = []
for i in np.arange(len(words)):
    words_for_version2.append([words[i][0],words[i][3],0,0,'True'])
np.save('data_sourse/npy/words_for_version2.npy',words_for_version2)
