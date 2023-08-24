import numpy as np
from function import get_colors,Ternary_to_Decimal
from tqdm import tqdm

words = np.load("data_sourse/npy/words.npy",allow_pickle=True)
length = len(words)

all_colors = np.zeros((length,length)).astype('i4')
for i in tqdm(range(length)):
    for j in np.arange(length):
        all_colors[i][j] = Ternary_to_Decimal(get_colors(words[i][0],words[j][0]))
np.save('data_sourse/npy/all_colors.npy',all_colors)