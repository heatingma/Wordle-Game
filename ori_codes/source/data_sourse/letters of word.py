import numpy as np
import pandas as pd

letter_num = pd.read_excel('data_sourse/file\letter_num.xlsx')
letter_num = np.squeeze(np.array(letter_num))
game_words = pd.read_excel('data_sourse/file\game_words.xlsx')
game_words = np.squeeze(np.array(game_words))

score_words = []
for i in np.arange(len(game_words)):
    word = game_words[i]
    letter_box = np.zeros(26)
    for j in np.arange(5):
        id = ord(word[j]) - 97
        letter_box[id] = 1/letter_num[id]
    sum = 0
    for k in np.arange(26):
        sum += letter_box[k]
    score_words.append([word,5/sum])
score_words = pd.DataFrame(score_words)
score_words.to_excel("data_sourse/file\score_words.xlsx")