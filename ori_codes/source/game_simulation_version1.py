import numpy as np
import copy
from function import *
from math import log 

ori_words = np.load("data_sourse\words_for_version1.npy")
length = len(ori_words)

def game_simulation_v1(answer:str,max_iter=100,use_favor_init=True,message=False,p=0.04,q=-9):
    sum_tries = 0
    tries = np.zeros(8)
    for _ in np.arange(max_iter):
        num = game_simulation_v1_real(answer,message=message,use_favor_init=use_favor_init,p=p,q=q)
        sum_tries += num
        tries[num-1] += 1
    average_tries = sum_tries / max_iter
    tries[7] = average_tries
    return tries

def game_simulation_v1_real(answer:str,message=False,use_favor_init=True,p=0.04,q=-9):
    favor_letter,favor_init = favor_init_word(p,q,1)
    words = copy.deepcopy(ori_words)
    tries = 0
    rand_begin = int(len(favor_init) * np.random.rand())
    while(True):
        if(tries == 0 and use_favor_init):
            sim_word = favor_init[rand_begin]
        else:
            #  generate random values
            rand_num = np.random.rand()

            # Find the corresponding word from the random value 
            # to simulate the word entered by the user
            for i in np.arange(length):
                if(words[i][2] == 'True'):
                    rand_num = rand_num - 2**float(words[i][1])
                    if(rand_num <= 0):
                        sim_word = words[i][0]
                        break

        # Judge whether the game is successful, 
        # If it fails, update the dictionary
        tries = tries + 1
        if(sim_word == answer or tries > 6):
            break
        else:
            update_words(words,sim_word,answer)
        if(message):
            left = []
            for i in np.arange(length):
                if(words[i][2] == 'True'):
                    left.append(words[i][0])
            print(left)
    return tries

def update_words(words,sim_word,answer):
    colors = get_colors(sim_word,answer)
    left_num = 0
    fre_sum = 0
    for i in np.arange(length):
        if(words[i][2] == 'True'):
            if(check_color(words[i][0],sim_word,colors) == False):
                words[i][2] = False
            else:                
                left_num += 1
                fre_sum += 2**(float(words[i][1]))
    for i in np.arange(length):
        if(words[i][2] == 'True'):
           words[i][1] = log(2**float(words[i][1])/fre_sum,2)
  
