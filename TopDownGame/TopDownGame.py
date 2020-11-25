# trying commiting from termianl

import traceback

import pygame, tkinter as tk
from pygame.locals import *
from tkinter import filedialog

MAPNAME = "TopDownGame/green_map/main.map"
# MAPNAME = "temp.map"
'''
screen_w = 1200
screen_h = 700
'''
screen_w, screen_h = 800, 600

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

font = None


class sprite:
    def __init__(self, surf, position, filename):
        self.surf = surf
        self.osurf = surf
        self.position = position
        self.rect = surf.get_rect()
        self.rect.topleft = position
        self.filename = filename
        self.type = 1  # 1-image
        self.angle = 0
        self.scale = 1.0
        self.collide = False
        self.oncollide = ""

    def rotate(self, angle):
        self.angle += angle
        t = self.rect.center
        self.surf = pygame.transform.rotozoom(self.osurf, self.angle, self.scale)
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
    def __init__(self, screen_w, screen_h):
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
        if frame_num % self.deltaframe == 0:
            self.num += 1
            if self.num == len(self.img_list):
                self.num = 0
        r_img = pygame.transform.rotate(self.img_list[self.num], angle)
        r_rect = r_img.get_rect()
        r_rect.center = (self.screen_w // 2, self.screen_h // 2)
        return r_img, r_rect

    def display_idle(self):
        # print("Display idle called !!")
        r_img = pygame.transform.rotate(self.img_list[0], self.angle)
        r_rect = r_img.get_rect()
        r_rect.center = (self.screen_w // 2, self.screen_h // 2)
        return r_img, r_rect


class TopDownGame:
    def __init__(self, screen):
        global font
        pygame.display.set_caption("TopDonwGame")
        self.screen = screen
        self.background_color = WHITE
        self.sprite_list = []
        self.static_list = []
        self.start_label_sprite = None
        self.font = pygame.font.SysFont(None, 24)
        font = self.font
        f = open(MAPNAME, 'r')
        print("Map in " + MAPNAME + " opened successfully")
        l = f.read()
        l = l.split('\n')
        for pos, j in enumerate(l[:-1]):
            i = j.split(",", 6)
            fn = i[0]
            if fn[0] == "I":
                surf = pygame.image.load('TopDownGame/' + fn[2:])
                surf = surf.convert_alpha()
                ts = sprite(surf, [0, 0], fn[2:])
                ts.rotate(float(i[3]))
                ts.changeSize(float(i[4]))
                ts.rect.topleft = [int(i[1]), int(i[2])]
                if str(i[5][2:]) == "True":
                    ts.collide = True
                ts.oncollide = i[6]
                self.sprite_list.append(ts)
                if pos == 0:
                    self.start_label_sprite = ts
            elif fn[0] == "T":
                print("appending static")
                self.static_list.append(Static(fn[2:], (int(i[1]), int(i[2]))))
        f.close()

        # setting the player
        self.player = Player(screen_w, screen_h)
        player_filenames = ["player_idle2.png", "player_walk_front_right2.png", "player_idle2.png", "player_walk_front_left2.png"]
        #player_filenames = ["player_walk_front_right2.png", "player_walk_front_left2.png"]
        for i in player_filenames:
            t_img = pygame.image.load('TopDownGame/' + i).convert()
            t_img.set_colorkey(t_img.get_at([5, 5]))
            t_rect = t_img.get_rect()
            t_rect.center = screen_w // 2, screen_h // 2
            self.player.add_img(t_img, t_rect)

    def TopDownGameLoop(self):
        playing = True

        moved_dir = [False] * 4
        start_rect = self.sprite_list[0].rect
        moved = [-start_rect.center[0] + 600, -start_rect.center[1] + 350]
        moved_old = moved.copy()

        angle = 0
        frame_num = 1
        up_frame_num = 1
        clock = pygame.time.Clock()
        while playing:
            self.screen.fill(self.background_color)

            should_move = True
            for i in self.sprite_list:
                if i.collide:
                    if (
                            i.rect.move(moved).colliderect(
                                self.player.rect_list[0])):  # technically the 0 should be player.num
                        should_move = False
                        if i.oncollide:
                            exec(eval(i.oncollide))
                        break
            if not should_move:
                moved = moved_old.copy()

            for i in self.sprite_list[1:]:
                self.screen.blit(i.surf, i.rect.move(moved))
            for i in self.static_list:
                # print("blitting static")
                self.screen.blit(i.surf, i.rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        playing = False
                    elif event.key == K_d:
                        moved_dir[0] = True
                    elif event.key == K_a:
                        moved_dir[1] = True
                    elif event.key == K_w:
                        moved_dir[2] = True
                    elif event.key == K_s:
                        moved_dir[3] = True

                elif event.type == KEYUP:
                    up_frame_num = 1
                    if event.key == K_d:
                        moved_dir[0] = False
                    elif event.key == K_a:
                        moved_dir[1] = False
                    elif event.key == K_w:
                        moved_dir[2] = False
                        # up_frame_num = 1
                    elif event.key == K_s:
                        moved_dir[3] = False

            moved_old = moved.copy()

            moving = False
            if moved_dir[0]:
                moved[0] -= 5
                moving = True
                angle = -90
                up_frame_num += 1
            elif moved_dir[1]:
                moved[0] += 5
                moving = True
                angle = 90
                up_frame_num += 1
            elif moved_dir[2]:
                moved[1] += 5
                up_frame_num += 1
                moving = True
                angle = 0
            elif moved_dir[3]:
                moved[1] -= 5
                moving = True
                up_frame_num += 1
                angle = 180

            if moving:
                self.screen.blit(*self.player.display(up_frame_num, angle))

            if not moving:
                self.screen.blit(*self.player.display_idle())

            # screen.blit(play_text_surf1, play_ts1_rect)
            # screen.blit(play_text_surf2, play_ts2_rect)

            pygame.display.update()
            frame_num += 1
            if frame_num == 61:
                frame_num = 1
            clock.tick(60)


if __name__ == "__main__":
    g = TopDownGame()
    g.TopDownGameLoop()
    print("End")
