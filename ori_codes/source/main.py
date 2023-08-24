import numpy as np
import pandas as pd
import copy
from tqdm import tqdm
from game_simulation_version1 import game_simulation_v1
from game_simulation_version2 import game_simulation_v2
game_words = np.load("data_sourse\game_words.npy",allow_pickle=True)
game_words = np.squeeze(game_words)


# computer_simulation_version_1
v1_tries = []
for i in tqdm(range(len(game_words)-350)):
    v1_tries.append(game_simulation_v1(game_words[i],use_favor_init=False))
c1_tries = np.array(v1_tries)
np.save("result/result_v1_2.npy",v1_tries)


"""
# computer_simulation_version_2
ori_words_v2 = np.load("data_sourse\words_for_version2.npy",allow_pickle=True)
best_init_v2 = np.load("data_sourse/best_init_words_for_version2.npy",allow_pickle=True)
for k in np.arange(len(best_init_v2)-1):
    v2_tries = []
    for i in tqdm(range(len(game_words))):
        ori_words_v2_copy = copy.deepcopy(ori_words_v2)
        v2_tries.append(game_simulation_v2(game_words[i],ori_words_v2_copy,best_init_v2[k+1]))
    v2_tries = np.array(v2_tries)
    np.save("result/result_v2_{}.npy".format(k+1),v2_tries)
"""
"""
#predict "eerie"

result_2 = []
for i in tqdm(range(5)):
    p = (i+1)/100
    for j in tqdm(range(5)):
        q = -8-j
        result = game_simulation_v1("eerie",max_iter=100,use_favor_init=False,p=p,q=q)
        result = np.concatenate([[p,q],result])
        result_2.append(result)
np.save("result/EERIE_different_pq.npy",result_2)
result_2 = pd.DataFrame(result_2)
result_2.to_excel("result/EERIE_different_pq.xlsx")
"""
"""
np.save("result/EERIE.npy",result)
result = pd.DataFrame(result)
result.to_excel("result/EERIE.xlsx")
"""