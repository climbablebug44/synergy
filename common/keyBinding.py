import os

import pygame


class keyBinding:
    def __init__(self):
        self.bindings = [pygame.K_a, pygame.K_d, pygame.K_b, pygame.K_q, pygame.K_e, pygame.K_w, pygame.K_s,
                         pygame.K_SPACE, pygame.K_r, pygame.K_f, pygame.K_t, pygame.K_z, 0, pygame.K_c]
        self.get()

    def get(self):
        try:
            with open('assets/keys.bin') as fp:
                self.bindings = eval(fp.read())
        except FileNotFoundError:
            pass

    def change(self, newL):
        self.bindings = newL
        self.commit()

    def commit(self, tempPath=''):
        if tempPath == '':
            tempPath = 'assets/keys.bin'
        with open(tempPath, 'w+') as fp:
            fp.write(self.bindings.__str__())

    def returnBindings(self):
        return self.bindings
