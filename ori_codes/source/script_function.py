import sys
import pygame as pg
import numpy as np
import pdb
import copy

def init_game():
    pg.init()

    screen_size = (800,600)
    bg_color = (230,230,230)
    screen = pg.display.set_mode(screen_size)
    
    submit_button = Button("Submit")
    pg.display.set_caption("Wordle Game")
    input_boxes = InputsquareBoxes(screen,275,100,50,50)
    pos_words_box = leftwordsBox(100,100,100,30,20)
    pos_words = np.load("data_sourse/npy\words_for_version2.npy",allow_pickle=True)
    pos_words_box.upgrade_pos_words(pos_words)
    output = textBox(300,400,200,50,40)
    answer = random_answer()
    
    while True:
        check_event(input_boxes,submit_button,answer,output)
        screen.fill(bg_color)
        draw(screen,[input_boxes,submit_button,output,pos_words_box])
        pg.display.flip()
        
class textBox:
    def __init__(self, x, y, w, h, font=60):
        self.rect = pg.Rect(x, y, w, h)
        self.color = pg.Color('lightskyblue3')
        self.text = ""
        self.FONT = pg.font.Font(None,font)
    
    def input(self,input):
        self.text = input
    
    def output_message(self,check,screen):
        if (check):
            self.text = "success!"
        else:
            self.text = "go ahead!"
        self.draw(screen)
                
    def draw(self, screen):
        text_surface = self.FONT.render(self.text,True,self.color)
        text_surface_rect = text_surface.get_rect()
        text_surface_rect.center = self.rect.center
        screen.blit(text_surface,text_surface_rect)
        pg.draw.rect(screen, self.color, self.rect, 2)

class Button:
    def __init__(self,msg):
        self.active = False
        self.width,self.height = 200,50
        self.button_color = (0,255,0)
        self.text_color = (255,0,255)
        self.font = pg.font.SysFont(None,48)
        self.rect = pg.Rect(300,500,self.width,self.height)
        self.prep_msg(msg)

    def prep_msg(self,msg):
        self.msg_image = self.font.render(msg,True,self.text_color,self.button_color)  
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center  
    
    def draw(self,screen):
        screen.fill(self.button_color,self.rect)
        screen.blit(self.msg_image,self.msg_image_rect)
    
    def check_active(self,x,y):
        if self.rect.collidepoint(x,y):
            self.active = True

class InputsquareBoxes:
    def __init__(self,screen, x, y, w, h):
        self.screen = screen
        self.squareBoxes = []
        self.check = False
        for i in range(5):
            yy = (h+2) * i + y
            self.squareBoxes.append(InputlineBox(x,yy,w,h))
        self.id = 0
        
    def handle_event(self,event:pg.event.Event,button:Button,answer,output_box:textBox):
        if(button.active):
            self.check = self.check_answer(answer)
            output_box.output_message(self.check,self.screen)
            self.id += min(4,self.id+1)
            button.active = False
        if(self.check == False):
            self.squareBoxes[self.id].handle_event(event)
    
    def check_answer(self,answer):
        return self.squareBoxes[self.id].check_answer(answer)
    
    def draw(self, screen):
        for i in range(5):
            self.squareBoxes[i].draw(screen)
        
class InputlineBox:
    def __init__(self, x, y, w, h):
        self.rects = []
        for i in range(5):
            xx = x+(w+2)*i
            self.rects.append(textBox(xx, y, w, h))
        self.rect_id = 0
        self.word = ""
        
    def handle_event(self,event:pg.event.Event):
        if event == pg.K_BACKSPACE:
            self.rect_id = max(0,self.rect_id-1)
            self.rects[self.rect_id].input("")
        elif(event.key >= 97 and event.key <= 122):
            if (self.rect_id <= 4):
                letter = chr(event.key-32)
                self.word += chr(event.key)
                self.rects[self.rect_id].input(letter)               
                self.rect_id += 1
    
    def check_answer(self,answer):
        if(self.word == answer):
            return True
        return False
    
    def draw(self, screen):
        for i in range(5):
            self.rects[i].draw(screen)

class leftwordsBox:
    def __init__(self, x, y, w, h, font=30):
        self.rects = []
        for i in range(10):
            yy = (h+2) * i + y
            self.rects.append(textBox(x,yy,w,h,font=font))

    def upgrade_pos_words(self,pos_words):
        self.pos_words = pos_words
        self.top = self.sort()
        self.output_top()     
        
    def sort(self):
        length = len(self.pos_words)
        top = []
        for i in range(min(10,length)):
            for j in range(length-i-1):
                if(float(self.pos_words[i][1]) < float(self.pos_words[j+i+1][1])):
                    tmp = copy.deepcopy(self.pos_words[i])
                    self.pos_words[i] = copy.deepcopy(self.pos_words[j+i+1])
                    self.pos_words[j+i+1] = copy.deepcopy(tmp)
                    flag = False
            top.append([self.pos_words[i][0],self.pos_words[i][1]])
        return top
    
    def output_top(self):
        for i in range(len(self.top)):
            fre = 2**float(self.top[i][1]) * 100
            self.rects[i].input(self.top[i][0] + " " + str(round(fre,2)) + "%")
                
    def draw(self, screen):
        for i in range(len(self.top)):
            self.rects[i].draw(screen)

def check_event(input_box:InputsquareBoxes,submit:Button,answer:str,output:textBox):
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit
        elif event.type == pg.MOUSEBUTTONDOWN:
            mouse_x,mouse_y = pg.mouse.get_pos()
            submit.check_active(mouse_x,mouse_y)
        elif event.type == pg.KEYDOWN:
            input_box.handle_event(event,submit,answer,output)
    
def random_answer():
    game_words = np.load("data_sourse/npy/game_words.npy",allow_pickle=True)
    id = int(len(game_words) * np.random.rand())
    return game_words[id][0]
        
def draw(screen,list:list):
    for i in range(len(list)):
        list[i].draw(screen)