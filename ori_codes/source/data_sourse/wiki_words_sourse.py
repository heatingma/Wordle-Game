import numpy as np
import pandas as pd
"""
def str_to_list(line:str):
    return_array = []
    current_words = ""
    for i in np.arange(len(line)):
        if(line[i] == '\n'):
            return_array.append(current_words)
            return return_array
        if(line[i]!= ' '):
            current_words = current_words + line[i]
        else:
            return_array.append(current_words)
            current_words = ""

def check_word(word):
    for i in np.arange(5):
        if(word[i]>'z' or word[i]<'a'):
            return False
    return True

with open('data_sourse/file/frequency from wikipedia.txt','r',encoding='UTF-8') as f:
    line = f.readline()
    line_array = str_to_list(line)
    wiki_words = []
    wiki_words.append(line_array)
    while(line):
        line = f.readline()
        wiki_words.append(str_to_list(line))
wiki_words = np.array(wiki_words,dtype='object')

words = []
for i in np.arange(len(wiki_words)-1):
    if(int(wiki_words[i][1]) == 5):
        word = wiki_words[i][0]
        if(check_word(word)):
            words.append([word,wiki_words[i][2]])

words = np.array(words)
words = pd.DataFrame(words)
words.to_excel('data_sourse/frequency from wilipedia.xlsx')
"""
######  Manual operation of Excel  ####
words = pd.read_excel("data_sourse/file/frequency from wilipedia.xlsx")
words = np.array(words)
np.save("data_wourse/wiki_words",words)