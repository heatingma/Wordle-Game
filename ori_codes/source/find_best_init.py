import numpy as np
ori_words = np.load("data_sourse/first_cal_entropy.npy",allow_pickle=True)

best_words = []
for i in np.arange(len(ori_words)):
    if(float(ori_words[i][2]) > 5.61):
        best_words.append(ori_words[i][0])
np.save("data_sourse/best_init_words_for_version2.npy",best_words)
print(best_words)