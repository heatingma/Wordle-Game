import numpy as np
from math import log
import sys
import pygame as pg
import copy

#############################################################
####                    SRM function                     ####
#############################################################

all_colors = np.load("all_colors.npy", allow_pickle=True)
game_words = np.load("wordle_words.npy", allow_pickle=True)
game_words = np.squeeze(game_words)
words = np.load("words.npy", allow_pickle=True)

def random_answer():
    id = int(len(game_words) * np.random.rand())
    return game_words[id]

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
        for k in np.arange(243):
            fre_dict[k] /= sum_fre
            if(fre_dict[k]!=0):
                info_entropy += fre_dict[k] * log(1/fre_dict[k] ,  2)
        ori_words[i][2] = info_entropy
    
        if(ori_words[i][4] == 'True'):
            ori_words[i][3] = 2**float(ori_words[i][1]) + float(ori_words[i][2])
        else:
            ori_words[i][3] = ori_words[i][2]
    return ori_words

def get_colors(word, answer):
    colors = np.zeros(5).astype('i4')
    used = np.zeros(5).astype('i4')
    for i in np.arange(5):
        letter = word[i]
        for j in np.arange(5):
            if(used[j] == 1):
                continue
            if(answer[j] == letter):
                if(i == j):
                    colors[i] = 2
                else:
                    colors[i] = 1
                used[j] = 1
                break
    return colors

def real_colors(colors):
    real_colors = np.empty(5).astype("str")
    translate = ['gray', 'gold', 'green']
    for i in np.arange(5):
        real_colors[i] = translate[colors[i]]
    return real_colors

def check_color(word1, word2, colors):
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

def update_words(word, colors, ori_words, pos_words):
    sum_freq = 0
    pos_words = []
    for i in np.arange(len(ori_words)):
        if(ori_words[i][4] == 'True'):
            if(check_color(ori_words[i][0], word, colors)):
                sum_freq = sum_freq + 2**float(ori_words[i][1])
            else:
                ori_words[i][4] = 'False'
    for i in np.arange(len(ori_words)):
        if(ori_words[i][4] == 'True'):
            fre = log((2**float(ori_words[i][1])) / sum_freq, 2)
            pos_words.append([ori_words[i][0], fre, 0, 0, 'True'])
            ori_words[i][1] = fre
    pos_words = np.array(pos_words)
    return ori_words, pos_words


#############################################################
####                    game function                    ####
#############################################################

def sort_words(words, key=1, num=10):
    length = len(words)
    top = []
    for i in range(min(num, length)):
        for j in range(length-i-1):
            if(float(words[i][key]) < float(words[j+i+1][key])):
                tmp = copy.deepcopy(words[i])
                words[i] = copy.deepcopy(words[j+i+1])
                words[j+i+1] = copy.deepcopy(tmp)
        top.append(words[i])
    return top

def set_format(string:str, length):
    length_string = len(string)
    format_string = string
    for i in np.arange(length-length_string):
        format_string += " "
    return format_string

def is_word(word):
    for i in np.arange(len(words)):
        if (words[i] == word):
            return True
    return False

def check_hard(word, pos_words):
    for i in np.arange(len(pos_words)):
        if(pos_words[i][0] == word):
            return True
    return False

def search_word(word):
    possible = []
    length = len(word)
    num = 0
    possible = ''
    for i in range(len(game_words)):
        flag = True
        for j in range(length):
            if(game_words[i][j] != word[j]):
                flag = False
        if(flag):
            if(num % 10 == 0 and num != 0):
                possible += '\n'
            possible += game_words[i] + '  '
            num += 1
        if(num >= 100):
            possible += '\n\nToo many words meet the conditions...'
            break
    if(num == 0):
        possible = 'No eligible words!'
    return possible

def check_event(button:list, input=None):
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
        elif event.type == pg.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pg.mouse.get_pos()
            for i in range(len(button)):
                button[i].check_active(mouse_x, mouse_y)
        elif event.type == pg.KEYDOWN:
            if(event.key == 13):
                if(button[0].msg == "Submit" or button[0].msg == 'Search'):
                    button[0].active = True
            if(input):
                input.handle_event(event)

def draw(screen, list:list):
    for i in range(len(list)):
        list[i].draw(screen)
        
def create():
    game = Wordle_game() 
    screen_size = (800, 600)
    screen_color = pg.Color((230, 230, 230))
    screen = pg.display.set_mode(screen_size)
    title = textBox(250, 50, 300, 60, font=40, color=screen_color, font_color='red')
    
    #menu
    play_button = Button(300, 200, 200, 40, "Play Game", font=20, button_color='paleturquoise', text_color='black')
    rule_button = Button(300, 260, 200, 40, "Game Rules", font=20, button_color='paleturquoise', text_color='black')
    set_button = Button(300, 320, 200, 40, "Game Settings", font=20, button_color='paleturquoise', text_color='black')
    lexicon_button = Button(300, 380, 200, 40, "Lexicon", font=20, button_color='paleturquoise', text_color='black')
    exit_button = Button(300, 440, 200, 40, "Exit", font=20, button_color='paleturquoise', text_color='black')
    return_button = Button(650, 520, 80, 30, "Menu", font=18, button_color='paleturquoise', text_color='black')
    
    #rule
    rule_box = textBox(100, 100, 600, 400, font=16, color=screen_color, font_color='black', 
                       x_format='left', y_format='up', y_space=9)
    
    #lexicon_box
    setting_box = textBox(200, 200, 400, 200, font=16, color=screen_color, font_color='black')
    search_title = textBox(100, 120, 100, 30, font=16, color=screen_color, font_color='black')
    search_box = lineBoxes(210, 120, 30, 30, font=16, color='aliceblue')
    search_button = Button(380, 120, 80, 30, "Search", font=14, button_color='paleturquoise', text_color='black')
    lexicon_box = textBox(100, 200, 600, 400, font=16, color=screen_color, font_color='black', 
                          font_name='SimSun', x_format='left', y_format='up')
    #end
    try_again = Button(300, 280, 200, 50, "Try again", font=30, button_color='paleturquoise', text_color='black')
    end_box = textBox(175, 150, 450, 50, font=30, color=screen_color, font_color='red')
    
    return game, screen, title, play_button, rule_button, set_button, lexicon_button, exit_button, return_button, \
    rule_box, setting_box, search_title, search_box, search_button, lexicon_box, try_again, end_box

def setting_create():
    #settings
    screen_color = pg.Color((230, 230, 230))
    settings_title = textBox(300, 150, 200, 50, font=30, color=screen_color, font_color='black')
    model = textBox(150, 250, 150, 50, font=24, color=screen_color, font_color='black')
    model_normal = Button(350, 260, 120, 30, "Normal", font=20, button_color='deepskyblue', text_color='black')
    model_hard = Button(500, 260, 120, 30, "Hard", font=20, button_color='aliceblue', text_color='black')
    help = textBox(150, 350, 150, 50, font=24, color=screen_color, font_color='black')
    help_no = Button(350, 360, 120, 30, "No", font=20, button_color='aliceblue', text_color='black')
    help_yes = Button(500, 360, 120, 30, "Yes", font=20, button_color='deepskyblue', text_color='black')
    return settings_title, model, model_normal, model_hard, help, help_no, help_yes
   
def game_create(screen):
    screen_color = pg.Color((230, 230, 230))
    submit_button = Button(325, 520, 150, 30, "Submit", button_color='paleturquoise', font=24, text_color='black')
    input = squareBoxes(screen, 250, 130, 55, 55)
    output = textBox(200, 465, 400, 40, font=20, color=screen_color, font_color='red')
    tip = textBox(200, 430, 400, 30, font=16, color=screen_color, font_color='black')
    pos_box = listBoxes(50, 100, 150, 30, title="Frequency", font=16, color=screen_color, 
                        font_color='black', font_name='CascadiaCode.ttf', ttf=True)
    help_box = listBoxes(600, 100, 150, 30, title="Entropy", font=16, color=screen_color, 
                         font_color='black', font_name='CascadiaCode.ttf', ttf=True, x_format='left')
    return_box = textBox(300, 200, 200, 100, font=24, color='aliceblue', font_color='black', y_format='up')
    save_Yes = Button(325, 250, 50, 30, "Yes", font=16, button_color='lightcyan', text_color='black')
    save_No = Button(425, 250, 50, 30, "No", font=16, button_color='lightcyan', text_color='black')
    return submit_button, input, output, tip, pos_box, help_box, return_box, save_Yes, save_No

def update_screen(list:list):
    screen.fill((230, 230, 230))
    title.input("Wordle Game")
    draw(screen, list)
    pg.display.flip()

#############################################################
####                    page function                    ####
#############################################################
def menu():
    while(True):
        list = [play_button, rule_button, set_button, lexicon_button, exit_button]
        respond = ['play', 'rule', 'setting', 'lexicon', 'exit']
        check_event(list)
        if(exit_button.active):
            sys.exit()
        list2 = [play_button, rule_button, set_button, lexicon_button, exit_button, title]
        update_screen(list2)
        for i in range(len(list)-1):
            if (list[i].active):
                game.change_page(respond[i])
                list[i].active = False
                return        

def rule():
    message = "Step1: Enter a 5-letter word.\n"
    message += "  (1) You'll have 6 chances to guess the 5-letter word of the day,  so make every guess count!\n" 
    message += "  (2) Try using a word that contains many different letters to narrow down your future guesses.\n" 
    message += "  (3) Type your first guess,  and then press or click Enter to see if you've matched any letters.\n"
    message += "\nStep2: Check the tile colors.\n"
    message += "After you make a guess,  the tile colors will change:\n"
    message += "  (1) A green tile indicates that you've guessed the correct letter in the correct place in the word.\n"
    message += "  (2) A yellow tile means you've guessed a letter that's in the word,  but not in the right spot.\n"
    message += "  (3) A gray tile means that letter is not in today's word.\n" 
    message += "\nStep3: Guess another word.\n"
    message += "  (1) Use the clues you got from your first guess to try again.\n" 
    message += "  (2) Continue entering your guesses until all letters are green.\n"

    while(True):
        check_event([return_button])
        if(return_button.active):
            return_button.active = False
            game.change_page('menu')
            return
        rule_box.input(message)
        list2 = [rule_box, title, return_button]
        update_screen(list2)

def setting(settings_title, model, model_normal, model_hard, help, help_no, help_yes):
    settings_title.input("Settings")
    model.input("Model:")
    help.input("Prompt box:")
    while(True):
        check_event([return_button, model_normal, model_hard, help_no, help_yes])
        if(return_button.active):
            return_button.active = False
            game.change_page('menu')
            return
        elif(model_normal.active):
            model_normal.active = False
            if(game.model != "Normal"):
                model_normal.change_color("deepskyblue")
                model_hard.change_color('aliceblue')
                game.model = "Normal"
        elif(model_hard.active):
            model_hard.active = False  
            if(game.model != "Hard"):
                model_hard.change_color("deepskyblue")
                model_normal.change_color('aliceblue')
                game.model = "Hard"
        elif(help_no.active):
            help_no.active = False 
            if(game.help):
                help_no.change_color("deepskyblue")
                help_yes.change_color('aliceblue')
                game.help = False
        elif(help_yes.active):
            help_yes.active = False  
            if(game.help == False):
                help_yes.change_color("deepskyblue")
                help_no.change_color('aliceblue')
                game.help = True
        list2 = [settings_title, model, model_normal, model_hard, help, help_no, help_yes, title, return_button]
        update_screen(list2)
        
def lexicon(search_button):
    lexicon_box.input('')
    search_box.clean()
    txt = "You can search any word in the lexicon."
    while(True):
        check_event([search_button, return_button], input=search_box)
        if(return_button.active):
            return_button.active = False
            search_box.clean()
            game.change_page('menu')
            return
        if(search_button.active):
            search_button.active = False
            word = search_box.word
            txt = search_word(word)    
        lexicon_box.input(txt)
        search_title.input('Enter letters:')
        list2 = [lexicon_box, title, return_button, search_box, search_title, search_button]
        update_screen(list2)

def wordle_game(submit_button, input, output, tip, pos_box, help_box, return_box, 
                save_Yes, save_No, answer, ori_words, pos_words):
    if(game.help and game.new_game):
        game.new_game = False
        top_entropy = copy.deepcopy(sort_words(copy.deepcopy(ori_words), key=2))
        top_frequency = copy.deepcopy(sort_words(copy.deepcopy(ori_words), key=1))
        pos_box.input(top_frequency, name="frequency")
        help_box.input(top_entropy, name="entropy")
        tip.input("The number of left words is " + str(len(pos_words)))
    while True:
        check_event([submit_button, return_button], input)
        
        if(return_button.active):
            while True:
                return_box.input("save the game?")
                check_event([save_Yes, save_No])
                if(save_Yes.active):
                    game.change_new_game(False)
                    game.save_last_game(answer, ori_words, pos_words, pos_box, help_box)
                    save_Yes.active = False
                    break
                elif(save_No.active):
                    game.change_new_game(True)
                    save_No.active = False
                    break
                if(game.help):
                    update_screen([input, title, submit_button, output, tip, pos_box, help_box, 
                               return_button, return_box, save_Yes, save_No])
                else:
                    update_screen([input, title, submit_button, output, tip, return_button, return_box, save_Yes, save_No])
            return_button.active = False
            game.change_page('menu')
            return 
        
        if(game.help):
            update_screen([input, title, submit_button, output, tip, pos_box, help_box, return_button])
        else:
            update_screen([input, title, submit_button, output, tip, return_button])
                
        if (submit_button.active):
            word = input.submit_word()
            if(word == answer):
                game.tries = input.id + 1
                colors = real_colors(get_colors(word=word, answer=answer))
                input.change_colors(colors)
                input.check = True
                output.input("Success!")
                submit_button.active = False
                submit_button.check = True
                if(game.help):
                    update_screen([input, title, submit_button, output, tip, pos_box, help_box, return_button])
                else:
                    update_screen([input, title, submit_button, output, tip, return_button])
                pg.time.delay(1000)
                game.change_page('end')
                return
            
            elif(is_word(word) and (game.model == "Normal" or check_hard(word, pos_words))):
                if(input.id == 4):
                    output.input("Game Over!")
                    if(game.help):
                        update_screen([input, title, submit_button, output, tip, pos_box, help_box, return_button])
                    else:
                        update_screen([input, title, submit_button, output, tip, return_button])
                    pg.time.delay(2000)
                    output.input("The answer is \"" + str(answer)+"\"")
                    if(game.help):
                        update_screen([input, title, submit_button, output, tip, pos_box, help_box, return_button])
                    else:
                        update_screen([input, title, submit_button, output, tip, return_button])  
                    pg.time.delay(5000)                  
                    game.change_page('end')
                    return
                colors = real_colors(get_colors(word=word, answer=answer))
                input.change_colors(colors)
                submit_button.active = False
                input.id = min(4, input.id+1)
                colors = get_colors(word, answer)
                ori_words, pos_words = update_words(word, colors, ori_words, pos_words)
                output.input("Input Error,  please continue the game")
                tip.input("The number of left words is " + str(len(pos_words)))
                pos_box.input_msg("calculating...")
                help_box.input_msg("calculating...")
                top_frequency = sort_words(copy.deepcopy(pos_words), key=1)
                pos_box.input(top_frequency, name="frequency")
                if(game.help):
                    update_screen([input, title, submit_button, output, tip, pos_box, help_box, return_button])
                else:
                    update_screen([input, title, submit_button, output, tip, return_button])
                    
                if(game.help):
                    if(len(pos_words) == 1):
                        help_box.input_msg("Only one word left!")
                    else:
                        ori_words = cal_info_entropy(ori_words)
                        top_entropy = sort_words(copy.deepcopy(ori_words), key=3, num=min(10, len(pos_words)))
                        help_box.input(top_entropy, name="entropy")
                        update_screen([input, title, submit_button, output, tip, pos_box, help_box, return_button])
            else:
                output.input("\"" + word.capitalize() + "\" is not a lagal-input-word!")
                submit_button.active = False

def end():
    game.new_game = True
    while True:
        check_event([try_again, exit_button, return_button])
        if(try_again.active):
            try_again.active = False
            game.change_page('play')
            return
        elif(exit_button.active):
            sys.exit()
        elif(return_button.active):
            return_button.active = False
            game.change_page('menu')
            return
        end_box.input('Thanks for playing the game!')
        list2 = [try_again, title, exit_button, title, end_box, return_button]
        update_screen(list2)  

#############################################################
####                       class                         ####
#############################################################
       
class Button:
    def __init__(self,  x,  y,  w,  h,  msg,  font_name="Times New Roman",  
                 font=24,  button_color=(0,  255,  0),  text_color=(255,  255,  255), 
                 border_radius=15,  border_width=2,  border_color="#b0ceeb"):
        self.active = False
        self.check = False
        self.button_color = pg.Color(button_color)
        self.text_color = pg.Color(text_color)
        self.border_radius = border_radius
        self.border_width = border_width
        self.border_color = pg.Color(border_color)
        self.font = pg.font.SysFont(font_name,  font)
        self.rect = pg.Rect(x,  y,  w,  h)
        self.msg = msg
        self.show = True
        self.force_check = False
        self.prep_msg(msg)

    def prep_msg(self,  msg):
        self.msg_image = self.font.render(msg,  True,  self.text_color,  self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def change_color(self,  color):
        self.button_color = color
        self.prep_msg(self.msg)

    def draw(self,  screen):
        if self.show:
            border_rect = self.rect.copy()
            border_rect.inflate_ip(self.border_width * 2,  self.border_width * 2)
            pg.draw.rect(screen,  self.border_color,  border_rect,  border_radius=self.border_radius)
            pg.draw.rect(screen,  self.button_color,  self.rect,  border_radius=self.border_radius)
            screen.blit(self.msg_image,  self.msg_image_rect)

    def check_active(self,  x,  y):
        if self.check == False:
            if self.rect.collidepoint(x,  y):
                self.active = True
            
class textBox:
    def __init__(self,  x,  y,  w,  h,  font=20, color='white', font_color='black'
                 , font_name="Times New Roman", ttf=False, x_format='center', y_format='center'
                 , x_space=5, y_space=5, border_radius=10, bold=True, italic=False, 
                 border=False, border_width=2, border_color="black", psw=False):
        self.rect = pg.Rect(x,  y,  w,  h)
        self.click =  False
        self.color = pg.Color(color)
        self.font_color = pg.Color(font_color)
        self.text = ""
        self.psw = psw
        self.write = True
        self.ttf = ttf
        self.bold = bold
        self.italic = italic
        self.font_name = font_name
        self.border = border
        self.border_width = border_width
        self.border_color = border_color
        if self.ttf:
            self.FONT = pg.font.Font(self.font_name, font)
            self.FONT.set_bold(self.bold)
            self.FONT.set_italic(self.italic)
        else:
            self.FONT = pg.font.SysFont(name=self.font_name, size=font, bold=self.bold, italic=self.italic)
        self.x_format = x_format
        self.y_format = y_format
        self.x_space = x_space
        self.y_space = y_space
        self.border_radius = border_radius
        self.show = True
        
    def check_active(self, x, y):
        if(self.click == False):
            if self.rect.collidepoint(x, y):
                self.click = True  
                  
    def change_font_size(self, font_size):            
        if self.ttf:
            self.FONT = pg.font.Font(self.font_name, font_size)
            self.FONT.set_bold(self.bold)
            self.FONT.set_italic(self.italic)
        else:
            self.FONT = pg.font.SysFont(name=self.font_name, size=font_size, bold=self.bold, italic=self.italic)
            
    def input(self, input):
        if self.write:
            self.text = input
    
    def clear(self):
        self.text = ""
        
    def change_font_color(self, color):
        self.font_color = pg.Color(color)        
    
    def change_color(self, color):
        self.color = pg.Color(color)
    
    def handle_event(self, event:pg.event.Event):
        if self.write:
            if (event.key == pg.K_BACKSPACE):
                self.text = self.text[0:-1]
            elif(event.key == pg.K_ESCAPE):
                sys.exit()
            elif(event.key == 13):
                pass
            elif(event.key >= 0 and event.key <= 128):
                letter = chr(event.key)
                self.text += letter             
           
    def draw(self,  screen):
        if self.border:
            border_rect = self.rect.copy()
            border_rect.inflate_ip(self.border_width * 2,  self.border_width * 2)
            pg.draw.rect(screen,  self.border_color,  border_rect,  border_radius=self.border_radius)
            pg.draw.rect(screen,  self.color,  self.rect,  border_radius=self.border_radius)
        else:
            pg.draw.rect(screen,  self.color,  self.rect,  border_radius=self.border_radius)
        # 绘制文本
        if self.psw:
            masked_text = '•' * len(self.text)
        else:
            masked_text = self.text
        self.texts = []
        current_text = ''
        for i in range(len(masked_text)):
            if(masked_text[i] != '\n'):
                current_text += masked_text[i]
            else:
                self.texts.append(current_text)
                current_text = ''
        self.texts.append(current_text)
        length = len(self.texts)
        for i in range(length):
            current_text = self.texts[i]
            text_surface = self.FONT.render(current_text, True, self.font_color)
            text_surface_rect = text_surface.get_rect()
            if(self.x_format == 'center'):
                text_surface_rect.centerx = self.rect.centerx
            elif(self.x_format == 'left'):
                text_surface_rect.x = self.rect.x + self.x_space
            if(self.y_format == 'center'):
                space_height = (self.rect.h - length * text_surface_rect.h)/(length+1)
                text_surface_rect.y = self.rect.y + space_height*(i+1) + text_surface_rect.h*i
            elif(self.y_format == 'up'):
                space_height = self.y_space
                text_surface_rect.y = self.rect.y + space_height*(i+1) + text_surface_rect.h*i
            screen.blit(text_surface, text_surface_rect)
        
class lineBoxes:
    def __init__(self,  x,  y,  w,  h, font=20, color='white', font_color='black', 
                 font_name="Times New Roman", ttf=False, x_format='center', y_format='center'):
        self.rects = []
        for i in range(5):
            xx = x+(w+2)*i
            self.rects.append(textBox(x=xx,  y=y,  w=w,  h=h, font=font, \
                color=color, font_color=font_color, font_name=font_name, \
                ttf=ttf, x_format=x_format, y_format=y_format, border_radius=0))
        self.rect_id = 0
        self.word = ""
        
    def handle_event(self, event:pg.event.Event):
        if (event.key == pg.K_BACKSPACE):
            self.rect_id = max(0, self.rect_id-1)
            self.rects[self.rect_id].input(chr(32))
            self.word = self.word[0:-1]
        elif (event.key == pg.K_ESCAPE):
            sys.exit()
        elif(event.key >= 97 and event.key <= 122):
            if (self.rect_id <= 4):
                letter = chr(event.key-32)
                self.word += chr(event.key)
                self.rects[self.rect_id].input(letter)               
                self.rect_id += 1
    
    def clean(self):
        for i in range(5):
            self.rects[i].input('')
        self.rect_id = 0
        self.word = ""
            
    def submit_word(self):
        return self.word

    def change_colors(self, colors):
        for i in range(5):
            self.rects[i].change_color(colors[i])
            
    def draw(self,  screen):
        for i in range(5):
            self.rects[i].draw(screen)    

class listBoxes:
    def __init__(self, x, y, w, h, title=None, font=20, color='white', font_color='black', 
                 font_name="Times New Roman", ttf=False, x_format='center', y_format='center'):
        self.rects = []
        self.rects.append(textBox(x=x, y=y, w=w, h=h, font=font, color=color, \
            font_color=font_color, font_name=font_name, ttf=ttf, \
            x_format='center', y_format='center'))
        if(title):
            self.rects[0].input(title)
        else:
            self.rects[0].input("List")
            
        for i in range(10):
            yy = (h+2) * (i+1) + y
            self.rects.append(textBox(x=x, y=yy, w=w, h=h, font=font, color=color, \
                font_color=font_color, font_name=font_name, ttf=ttf, \
                x_format=x_format, y_format=y_format))

    def input(self, top, name=None):
        self.top = top
        for i in range(len(top)):
            if(name == "frequency"):
                frequency = 2**float(top[i][1])*100
                input = set_format(top[i][0], 7) + set_format(str(round(frequency, 2))+"%", 7)
            elif(name == "entropy"):
                word = set_format(top[i][0], 7)
                entropy = set_format(str(round(float(top[i][2]), 2)), 6)
                sum = set_format(str(round(float(top[i][3]), 2)), 7) 
                input = word + entropy + sum           
            else:
                input = str(top[i])
            self.rects[i+1].input(input)
            
    def input_msg(self, message:"str"):
        self.top = [message]
        self.rects[1].input(message)
                    
    def draw(self,  screen):
        for i in range(len(self.top)+1):
            self.rects[i].draw(screen)

class squareBoxes:
    def __init__(self, screen,  x,  y,  w,  h):
        self.screen = screen
        self.squareBoxes = []
        self.check = False
        for i in range(5):
            yy = (h+2) * i + y
            self.squareBoxes.append(lineBoxes(x, yy, w, h))
        self.id = 0
        
    def handle_event(self, event:pg.event.Event):
        if(self.check == False):
            self.squareBoxes[self.id].handle_event(event)
    
    def submit_word(self):
        return self.squareBoxes[self.id].submit_word()
    
    def change_colors(self, colors):
        self.squareBoxes[self.id].change_colors(colors)
    
    def draw(self,  screen):
        for i in range(5):
            self.squareBoxes[i].draw(screen)

class Wordle_game:
    def __init__(self):
        self.page = "menu"
        self.new_game = True
        self.model = "Normal"
        self.help = True
        self.save = []
        self.have_set = False
        self.tries = None
        
    def change_page(self, page):
        self.page = page
        
    def settings(self, model="Normal", help=False):
        self.model = model
        self.help = help
   
    def change_new_game(self, new_game):
        self.new_game = new_game

    def save_last_game(self, answer, ori_words, pos_words, pos_box, help_box):
        self.save = [answer, ori_words, pos_words, pos_box, help_box]
    
    def last_game(self):
        return self.save[0], self.save[1], self.save[2], self.save[3], self.save[4]


#############################################################
####                     main game                       ####
#############################################################

pg.init()
pg.display.set_caption("Wordle Game")

game, screen, title, play_button, rule_button, set_button, lexicon_button, exit_button, \
return_button, rule_box, setting_box, search_title, search_box, search_button, lexicon_box, \
try_again, end_box= create()

while True:
    if(exit_button.active == True):
        sys.exit()
    if(game.page == 'menu'):
        menu()
    elif(game.page == 'rule'):
        rule()
    elif(game.page == 'setting'):
        if(game.have_set == False):
            settings_title, model, model_normal, model_hard, help, help_no, help_yes = setting_create()
            game.have_set = True
        setting(settings_title, model, model_normal, model_hard, help, help_no, help_yes)
        
    elif(game.page == 'lexicon'):
        lexicon(search_button)  
    elif(game.page == 'play'):
        if(game.new_game == True):
            submit_button, input, output, tip, pos_box, help_box, return_box, save_Yes, save_No = game_create(screen)
            answer = random_answer()
            ori_words = np.load("first_cal_entropy.npy", allow_pickle=True)
            pos_words = copy.deepcopy(ori_words)
        else:
            answer, ori_words, pos_words, pos_box, help_box = game.last_game()
        wordle_game(submit_button, input, output, tip, pos_box, help_box, return_box, 
                    save_Yes, save_No, answer, ori_words, pos_words)
    elif(game.page == 'end'):
        end()

        
