import numpy as np
from math import log
import pandas as pd


wordle_words = np.load('data_sourse/npy/wordle_words.npy',allow_pickle=True)
kaggle_words = np.load('data_sourse/npy/kaggle_words.npy',allow_pickle=True)
wiki_words = np.load('data_sourse/npy/wiki_words.npy',allow_pickle=True)

words = []
for i in np.arange(len(wordle_words)):
    words.append([wordle_words[i][0],0,0,0])
words = np.array(words)
length = len(words)

i = 0
sum_wiki_fre = 0
for j in np.arange(len(wiki_words)):
    if(wiki_words[j][0] == words[i][0]):
        words[i][1] = wiki_words[j][1]
        sum_wiki_fre = sum_wiki_fre + float(wiki_words[j][1])
        i = i+1
        if(i == length):
            break
        
for j in np.arange(length):
    words[j][1] = log(float(words[j][1]) / sum_wiki_fre,2)

i = 0
sum_kaggle_fre = 0
for j in np.arange(len(kaggle_words)):
    if(kaggle_words[j][0] == words[i][0]):
        words[i][2] = kaggle_words[j][1]
        sum_kaggle_fre = sum_kaggle_fre + float(kaggle_words[j][1])
        i = i+1
        if(i == length):
            break
        
for j in np.arange(length):
    words[j][2] = log(float(words[j][2]) / sum_kaggle_fre,2)
    words[j][3] = log( ( 2**(float(words[j][1])) + 2**(float(words[j][2])) )/2 ,2)
    
np.save("data_sourse/npy/words.npy",words)
words = pd.DataFrame(words)
#words.to_excel("data_sourse/file/words_frequency.xlsx")