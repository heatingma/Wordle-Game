import numpy as np
import copy
from math import log
from function import *
import pdb

def game_simulation_v2(answer:str,ori_words,best_init):
    tries = 0
    pos_words = copy.deepcopy(ori_words)
    while(tries < 7):
        if(tries == 0):
            sim_word = best_init
        else:
            len_pos_words= len(pos_words)
            if(len_pos_words>2): 
                ori_words = cal_info_entropy(ori_words)
                sim_word = select(pos_words,ori_words)
            elif(len_pos_words == 2):
                if(float(pos_words[0][1]) > float(pos_words[1][1])):
                    sim_word = pos_words[0][0]
                else:
                    sim_word = pos_words[1][0]
            else:
                sim_word = pos_words[0][0]
        tries = tries + 1
        if(sim_word == answer or tries > 6):
            return tries
        else:
            colors = get_colors(sim_word,answer)
            ori_words,pos_words = update_words(sim_word,colors,ori_words,pos_words)

def select(pos_words,ori_words):
    best_id = 0
    for i in np.arange(len(ori_words)):
        if(ori_words[i][4] == 'True'):
            for j in np.arange(len(pos_words)):
                if(ori_words[i][0] == pos_words[j][0]):
                    ori_words[i][3] = 2**float(pos_words[j][1]) + float(ori_words[i][2])
        else:
            ori_words[i][3] = ori_words[i][2]
        if(float(ori_words[i][3]) > float(ori_words[best_id][3])):
            best_id = i
    return ori_words[best_id][0]

def select_2(pos_words):
    sel_id = 0
    for i in np.arange(len(pos_words)):
        if(check_repeat(pos_words[i][0])):
            if(pos_words[i][1]>pos_words[sel_id][0]):
                sel_id = i
    if(sel_id == 0):
        if(check_repeat(pos_words[0][0]) == False):
            for i in np.arange(len(pos_words)):
                if(pos_words[i][1]>pos_words[sel_id][0]):
                    sel_id = i             
    return pos_words[sel_id][0]

def update_words(word,colors,ori_words,pos_words):
    sum_freq = 0
    pos_words = []
    for i in np.arange(len(ori_words)):
        if(ori_words[i][4] == 'True'):
            if(check_color(ori_words[i][0],word,colors)):
                sum_freq = sum_freq + 2**float(ori_words[i][1])
            else:
                ori_words[i][4] = 'False'
    for i in np.arange(len(ori_words)):
        if(ori_words[i][4] == 'True'):
            fre = (2**float(ori_words[i][1])) / sum_freq
            pos_words.append([ori_words[i][0],fre,0,0,'True'])
    pos_words = np.array(pos_words)
    return ori_words,pos_words