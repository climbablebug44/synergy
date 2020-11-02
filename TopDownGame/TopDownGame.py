#       THIS FILE IS INCOMPLETE , UPLOADED JUST TO TEST 

import pygame, tkinter as tk
from pygame.locals import *
from tkinter import filedialog

MAPNAME = "green_map/main.map"
#MAPNAME = "temp.map"

screen_w = 1200
screen_h = 700

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
BLUE = (0,0,255)

class sprite:
    def __init__(self, surf, position, filename):
        self.surf = surf
        self.osurf = surf
        self.position = position
        self.rect = surf.get_rect()
        self.rect.topleft = position
        self.filename = filename
        self.type = 1           # 1-image
        self.angle = 0
        self.scale = 1.0
        self.collide = False
        self.oncollide = ""

    def rotate(self, angle):
        self.angle += angle
        t = self.rect.center
        self.surf = pygame.transform.rotozoom( self.osurf, self.angle, self.scale)
        self.rect = self.surf.get_rect()
        self.rect.center = t

    def changeSize(self, scale):
        self.scale *= scale
        t = self.rect.center
        self.surf = pygame.transform.rotozoom(self.osurf, self.angle, self.scale)
        self.rect = self.surf.get_rect()
        self.rect.center = t

class Static:
    def __init__(self, text, position):
        self.text = text
        self.surf = font.render(text, True, BLACK)
        self.rect = self.surf.get_rect()
        self.rect.topleft = position

    def getText(self):
        return self.text

    def setText(self, text):
        self.text = text
        self.surf = font.render(self.text, True, BLACK)
        pos = self.rect.topleft
        self.rect = self.surf.get_rect()
        self.rect.topleft = pos

class Player:
    def __init__(self,screen_w,screen_h):
        self.img_list = []
        self.rect_list = []
        self.deltaframe = 7
        self.num = 0
        self.angle = 0
        self.screen_w = screen_w
        self.screen_h = screen_h

    def add_img(self, surf, rect):
        self.img_list.append(surf)
        self.rect_list.append(rect)

    def display(self, frame_num, angle):
        self.angle = angle
        if(frame_num % self.deltaframe == 0):
            self.num += 1
            if(self.num == len(self.img_list)):
                    self.num = 0
        r_img = pygame.transform.rotate(self.img_list[self.num],angle)
        r_rect = r_img.get_rect()
        r_rect.center = (self.screen_w//2,self.screen_h//2)
        return r_img, r_rect

    def display_idle(self):
        r_img = pygame.transform.rotate(self.img_list[0],angle)
        r_rect = r_img.get_rect()
        r_rect.center = (self.screen_w//2,self.screen_h//2)
        return r_img, r_rect


class TopDownGame:
    def __init__(self):
	pygame.init()
        pygame.display.set_caption("Map Maker")
        screen = pygame.display.set_mode((screen_w,screen_h))
