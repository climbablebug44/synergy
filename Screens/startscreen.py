import pygame
import common.gameConstants as gc
from common.keyBinding import keyBinding

"""
@author: climbablebug_44
Menu screens i have been working on, not added to project
ignore the following files and/or folders:

Screens/assets/keys.bin
common/keyBinding.py
Screens/startscreen.py

To check this menu run the file 'startscreen.py' as
python startscreen.py

navigation keys : arrow keys
"""


class startScreen(pygame.Surface):
    def __init__(self, size, screen, clock, mode='mainpage'):
        super().__init__(size)
        self.running = True
        self.mode = mode
        self.screen = screen
        self.screenSize = size
        self.font = pygame.font.Font('freesansbold.ttf', 30)
        self.theme = [gc.color['WHITE'], gc.color['BLACK']]
        self.clock = clock
        self.selected = 0

        self.pageLabels = {'mainpage': ['Play', 'Settings', 'Credits', 'Exit'],
                           'settings': ['Walk Left', 'Walk Right', 'Block', 'Light Attack', 'Heavy Attack',
                                        'Slot toggle Up', 'Slot Toggle Down', 'Jump', 'Reload', 'Special', 'Push',
                                        'Auto-Aim Shoot', 'Toggle Auto aim', 'Toggle selected enemy'],
                           'pause': ['Resume', 'Settings', 'Quit to Main Menu']}
        self.keyBind = keyBinding()

        self.defaultSize = {'mainpage': 30,
                            'settings': 30,
                            'pause': 30}
        self.offset = {'mainpage': 30,
                       'settings': 20,
                       'pause': 10}
        self.static = 0
        self.highlightMemory = -1
        self.history = self.mode

        while self.running:
            self.screen.fill(self.theme[1])
            if self.mode == 'mainpage':
                self.drawMainPage()
            elif self.mode == 'settings':
                self.drawSettings()
            elif self.mode == 'pause':
                self.drawPauseScreen()
            else:
                raise Exception('Invalid mode:' + self.mode)
            pygame.display.flip()
            self.clock.tick(60)

    def changeFontSize(self, x):
        self.font = pygame.font.Font('freesansbold.ttf', x)

    def drawText(self, text, position, color=()):
        text = self.font.render(text, True, self.theme[0])
        text_rect = text.get_rect()
        temp = text_rect.copy()
        temp.center = position
        temp.inflate_ip(self.offset[self.mode], self.offset[self.mode])
        y = temp.width
        if self.static < y:
            temp.inflate_ip((self.static - y), 0)
            self.static += 1
        text_rect.center = position
        if color != ():
            pygame.draw.rect(self.screen, color, temp)
        self.screen.blit(text, text_rect)

    def resetEverything(self):
        self.static = 0
        self.selected = 0

    @staticmethod
    def tupleMinus(a, b):
        return tuple(map(lambda x, y: x - y, a, b))

    @staticmethod
    def tuplePlus(a, b):
        return tuple(map(lambda x, y: x + y, a, b))

    def drawMainPage(self):
        self.changeFontSize(30)
        center = (self.screenSize[0] / 2, self.screenSize[1] / 2)
        for j in range(len(self.pageLabels[self.mode])):
            color = ()
            if j == self.selected:
                color = (100, 100, 100)
            self.drawText(self.pageLabels[self.mode][j], self.tuplePlus(center, (0, 53 * j)), color)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.pageLabels[self.mode])
                self.static = 0
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.pageLabels[self.mode])
                self.static = 0
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if self.selected == 0:
                    # play mechanism
                    pass
                elif self.selected == 1:
                    self.mode = 'settings'
                elif self.selected == 2:
                    self.mode = 'credits'
                elif self.selected == 3:
                    pygame.quit()
                    exit()
                self.resetEverything()

    def drawSettings(self):
        self.changeFontSize(40)
        key = self.keyBind.returnBindings()
        self.screen.fill(gc.color['BLACK'])
        self.drawText('Settings', (self.screenSize[0] // 2, 50))
        self.drawText('Controls', (250, 100))
        self.changeFontSize(15)
        for i in range(len(self.pageLabels[self.mode])):
            highlight = ()
            if i == self.selected:
                highlight = (100, 100, 100)
            self.drawText(self.pageLabels[self.mode][i], self.tuplePlus((100, 150), (150, 30 * i)), highlight)
            if i == self.highlightMemory:
                highlight = (128, 0, 0)
            else:
                highlight = ()
            self.drawText(pygame.key.name(key[i]), self.tuplePlus((450, 150), (500, 30 * i)), highlight)
        self.drawText('Press Backspace to save and exit, or Esc to reset everything back to default...',
                      (300, self.screenSize[1] - 15))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                # TODO: ESCAPE KEY WORKS ONLY ONCE
                print('hello')
                self.keyBind.setDefault()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
                self.keyBind.commit()
                self.mode = self.history
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.pageLabels[self.mode])
                self.static = 0
                self.highlightMemory = -1
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                self.static = 0
                self.highlightMemory = -1
                self.selected = (self.selected + 1) % len(self.pageLabels[self.mode])
            elif event.type == pygame.KEYDOWN:
                self.highlightMemory = -1
                temp = key[self.selected]
                key[self.selected] = event.key
                tempkeys = key.copy()
                tempkeys.sort()
                if tempkeys != sorted(list(set(key))):
                    self.highlightMemory = self.selected
                    key[self.selected] = temp
                self.keyBind.change(key)
            else:
                break

    def drawPauseScreen(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.pageLabels[self.mode])
                self.static = 0
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.pageLabels[self.mode])
                self.static = 0
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if self.selected == 0:
                    self.running = False
                elif self.selected == 1:
                    self.resetEverything()
                    self.history = self.mode
                    self.mode = 'settings'
                elif self.selected == 2:
                    self.resetEverything()
                    # TODO: SAVE GAME
                    self.history = 'mainpage'
                    self.mode = 'mainpage'

        self.screen.fill(gc.color['BLACK'])
        self.changeFontSize(20)
        for i in range(len(self.pageLabels[self.mode])):
            color = ()
            if self.selected == i:
                color = (100, 100, 100)
            self.drawText(self.pageLabels[self.mode][i],
                          self.tuplePlus((self.screenSize[0] // 2, self.screenSize[1] // 2), (0, 30 * i)), color)


sizeofScr = (800, 600)

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    sizeofScr = screen.get_size()
    clock = pygame.time.Clock()
    start = startScreen(sizeofScr, screen, clock, mode='pause')
