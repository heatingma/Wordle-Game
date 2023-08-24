import numpy as np
from math import log

all_colors = np.load("data_sourse/npy/all_colors.npy",allow_pickle=True)

def cal_info_entropy(ori_words):
    for i in np.arange(len(ori_words)):
        fre_dict = np.zeros(243)
        sum_fre = 0
        info_entropy = 0
        for j in np.arange(len(ori_words)):
            if(ori_words[j][4] == 'True'):
                freq = 2**float(ori_words[j][1])
                fre_dict[all_colors[i][j]] += freq
                sum_fre += freq
        if(i == 0):
            np.save("fre.npy",fre_dict)
        for k in np.arange(243):
            fre_dict[k] /= sum_fre
            if(fre_dict[k]!=0):
                info_entropy += fre_dict[k] * log(1/fre_dict[k] , 2)
        ori_words[i][2] = info_entropy
    return ori_words

def get_colors(word,answer):
    colors = np.zeros(5).astype('i4')
    used = np.zeros(5).astype('i4')
    for i in np.arange(5):
        if(word[i] == answer[i]):
            colors[i] = 2
            used[i] = 1
    for i in np.arange(5):
        if(colors[i] == 2):
            continue
        letter = word[i]
        for j in np.arange(5):
            if(letter == answer[j] and used[j] == 0):
                colors[i] = 1
                used[j] = 1
                break
    return colors

def check_color(word1,word2,colors):
    used = np.zeros(5).astype('i4')
    for i in np.arange(5):
        color = colors[i]
        letter = word2[i]
        if(color == 0):
            for j in np.arange(5):
                if(used[j]):
                    continue
                if(word1[j] == letter):
                    return False
        elif(color == 2):
            if(word1[i] != letter):
                return False
            else:
                used[i] = 1
        else:
            flag = False
            for j in np.arange(5):
                if(used[j]):
                    continue
                if(word1[j] == letter):
                    if(i != j):
                        used[j] = 1
                        flag = True
                        break
                    else:
                        return False
            if(flag == False):
                return False
    return True

def favor_init_word(p_letter_min=0.05,logp_word_min=-7,version=1):
    letter_num = np.load("data_sourse\letter_num.npy",allow_pickle=True)
    words = np.load("data_sourse\words.npy",allow_pickle=True)

    favor_letter = []
    for i in np.arange(26):
        if(letter_num[i] > p_letter_min):
            favor_letter.append(chr(i+97))
    favor_letter = np.array(favor_letter).astype('str')

    words_sel = []
    for i in np.arange(len(words)):
        if(float(words[i][3]) > logp_word_min):
            if(check_repeat(words[i][0])):
                words_sel.append(words[i][0])
    words_sel = np.array(words_sel)
    len_words_sel = len(words_sel)
    
    words_favor = []
    if(version == 1):
        for i in np.arange(len_words_sel):
            word = words_sel[i]
            if(check_in_letter(word,favor_letter)):
                words_favor.append(word)
    else:
        for i in np.arange(len_words_sel):
            word1 = words_sel[i]
            if(check_in_letter(word1,favor_letter)):
                for j in np.arange(len_words_sel-i-1):
                    word2 = words_sel[j+i+1]
                    if(check_in_letter(word2,favor_letter)):
                        if(check_words_repeat(word1,word2)):
                            words_favor.append([word1,word2])
    
    return favor_letter,words_favor


def check_in_letter(word,favor_letter):
    len_letter = len(favor_letter)
    for j in np.arange(5):
        letter = word[j]
        for k in np.arange(len_letter):
            if(favor_letter[k] == letter):
                break
        if(favor_letter[k] != letter):
            return False
    return True

def check_repeat(word):
    for i in np.arange(5):
        letter = word[i]
        for j in np.arange(4-i):
            if(letter == word[j+i+1]):
                return False
    return True

def check_words_repeat(word1,word2):
    for i in np.arange(5):
        letter = word1[i]
        for j in np.arange(5):
            if(letter == word2[j]):
                return False
    return True

def Decimal_to_Ternary(num):
    array = np.zeros(5).astype('i4')
    i = 0
    while(num>0):
        array[4-i] = num % 3
        num = int(num / 3)
        i = i+1
    return array       

def Ternary_to_Decimal(array):
    num = 0
    for i in np.arange(5):
        num += 3**(4-i) * array[i]
    return num
    