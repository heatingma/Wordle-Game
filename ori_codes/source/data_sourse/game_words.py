import pandas as pd
import numpy as np
import pdb
game_words = pd.read_excel("data_sourse/file/game_words.xlsx")
np.save('data_sourse/game_words.npy',game_words)

game_words = np.squeeze(np.array(game_words))
words_fre = pd.read_excel("data_sourse/file/words_frequency.xlsx")
words_fre = np.array(words_fre)
game_words_fre = []
for i in np.arange(len(game_words)):
    for j in np.arange(len(words_fre)):
        if(game_words[i] == words_fre[j][0]):
            game_words_fre.append(words_fre[j])
            break
np.save('data_sourse/game_words_frequency.npy',game_words_fre)
game_words_fre = pd.DataFrame(game_words_fre)
game_words_fre.to_excel('data_sourse/file/game_words_frequency.xlsx')

def num_repeat(word):
    letter_box = np.zeros(26)
    for i in np.arange(5):
        letter_box[ord(word[i])-97] = 1
    sum = 0
    for j in np.arange(26):
        sum += letter_box[j]
    return int(5-sum)

game_words_repeat = []
for i in np.arange(len(game_words)):
    game_words_repeat.append([game_words[i],num_repeat(game_words[i])])
np.save('data_sourse/game_words_repeat.npy',game_words_repeat)
game_words_repeat = pd.DataFrame(game_words_repeat)
game_words_repeat.to_excel('data_sourse/file/game_words_repeat.xlsx')