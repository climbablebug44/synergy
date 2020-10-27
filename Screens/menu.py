import pygame


class Menu():
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = - 100

    def draw_cursor(self):
        self.game.draw_text('(-)', 20, self.cursor_rect.x, self.cursor_rect.y)

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        image = pygame.image.load(r'Screens/Action-Mania.png')
        image = pygame.transform.scale(image, (450, 150))
        self.game.window.blit(image, (200, 0))
        pygame.display.update()
        self.game.reset_keys()


class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start"
        self.startx, self.starty = self.mid_w, self.mid_h + 30
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 65
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 100
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Main Menu', 35, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 25)
            self.game.draw_text("Start Game", 25, self.startx, self.starty)
            self.game.draw_text("Settings", 25, self.optionsx, self.optionsy)
            self.game.draw_text("Credits", 25, self.creditsx, self.creditsy)
            self.game.draw_text("Exit", 25, self.mid_w, self.mid_h + 130)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Settings'
            elif self.state == 'Settings':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.mid_w + self.offset, self.mid_h + 130)
                self.state = 'Exit'
            elif self.state == 'Exit':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state == 'Start'
        elif self.game.UP_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.mid_w + self.offset, self.mid_h + 130)
                self.state = 'Exit'
            elif self.state == 'Settings':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Settings'
            elif self.state == 'Exit':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == 'Start':
                self.game.playing = True
            elif self.state == 'Settings':
                self.game.curr_menu = self.game.options
            elif self.state == 'Credits':
                self.game.curr_menu = self.game.credits
            elif self.state == 'Exit':
                quit()
            self.run_display = False


class OptionsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Volume'
        self.volx, self.voly = self.mid_w, self.mid_h + 20
        self.controlsx, self.controlsy = self.mid_w, self.mid_h + 45
        self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
        # self.x, self.y, self.z, self.l, self.m, self.n, self.b, self.v, self.o, self.g = 'W', 'S', 'A', 'D', 'P', 'C', 'U', 'I', 'Space', 'Q'
        self.keys = ['W', 'S', 'A', 'D', 'P', 'C', 'U', 'I', 'Space','E','B','Q','Done']

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill((0, 0, 0))
            self.game.draw_text('Settings', 32, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 30)
            self.game.draw_text("Volume", 22, self.volx, self.voly)
            self.game.draw_text("Controls", 22, self.controlsx, self.controlsy)
            self.game.draw_text("Language", 22, self.mid_w, self.mid_h + 67)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.game.UP_KEY or self.game.DOWN_KEY:
            if self.state == 'Volume':
                self.state = 'Controls'
                self.cursor_rect.midtop = (self.controlsx + self.offset, self.controlsy)
            elif self.state == 'Controls':
                self.state = 'Language'
                self.cursor_rect.midtop = (self.mid_w + self.offset, self.mid_h + 67)
            elif self.state == 'Language':
                self.state = 'Volume'
                self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
        elif self.game.START_KEY:
            # TO-DO: Create a Volume Menu and a Controls Menu
            self.control()

    def control(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.game.display.fill((0, 0, 0))
            self.game.draw_text('Controls', 20, 50, 25)
            self.game.draw_text('Move Forward ', 15, 200, 50)
            self.game.draw_text('Move Backward', 15, 190, 80)
            self.game.draw_text('Left Move', 15, 210, 110)
            self.game.draw_text('Right Move', 15, 210, 140)
            self.game.draw_text('Pause', 15, 220, 170)
            self.game.draw_text('Continue', 15, 210, 200)
            self.game.draw_text('Cam Up', 15, 210, 230)
            self.game.draw_text('Side Cam', 15, 210, 260)
            self.game.draw_text('Backspace', 15, 205, 290)
            self.game.draw_text('Speed Up',15,210,320)
            self.game.draw_text('Fire ',15,230,350)
            self.game.draw_text('Quit', 15, 220, 380)
            self.game.window.blit(self.game.display, (0, 0))
            self.Change_controls()
            mouse = pygame.mouse.get_pos()
            smallfont = pygame.font.SysFont('Corbel', 18)
            text = smallfont.render(self.keys[0], True, [255, 255, 255])
            if 255 <= mouse[0] <= 320 and 40 <= mouse[1] <= 56:
                pygame.draw.rect(self.game.window, [120, 209, 147], [255, 40, 65, 16])
            else:
                pygame.draw.rect(self.game.window, [128, 123, 200], [255, 40, 65, 16])

            self.game.window.blit(text, (277, 40))

            text = smallfont.render(self.keys[1], True, [255, 255, 255])
            if 255 <= mouse[0] <= 320 and 70 <= mouse[1] <= 86:
                pygame.draw.rect(self.game.window, [120, 209, 147], [255, 70, 65, 16])
            else:
                pygame.draw.rect(self.game.window, [128, 123, 200], [255, 70, 65, 16])

            self.game.window.blit(text, (280, 70))

            text = smallfont.render(self.keys[2], True, [255, 255, 255])
            if 255 <= mouse[0] <= 320 and 100 <= mouse[1] <= 116:
                pygame.draw.rect(self.game.window, [120, 209, 147], [255, 100, 65, 16])
            else:
                pygame.draw.rect(self.game.window, [128, 123, 200], [255, 100, 65, 16])

            self.game.window.blit(text, (280, 100))

            text = smallfont.render(self.keys[3], True, [255, 255, 255])
            if 255 <= mouse[0] <= 320 and 130 <= mouse[1] <= 146:
                pygame.draw.rect(self.game.window, [120, 209, 147], [255, 130, 65, 16])
            else:
                pygame.draw.rect(self.game.window, [128, 123, 200], [255, 130, 65, 16])

            self.game.window.blit(text, (280, 130))

            text = smallfont.render(self.keys[4], True, [255, 255, 255])
            if 255 <= mouse[0] <= 320 and 160 <= mouse[1] <= 176:
                pygame.draw.rect(self.game.window, [120, 209, 147], [255, 160, 65, 16])
            else:
                pygame.draw.rect(self.game.window, [128, 123, 200], [255, 160, 65, 16])
            self.game.window.blit(text, (280, 160))

            text = smallfont.render(self.keys[5], True, [255, 255, 255])
            if 255 <= mouse[0] <= 320 and 190 <= mouse[1] <= 206:
                pygame.draw.rect(self.game.window, [120, 209, 147], [255, 190, 65, 16])
            else:
                pygame.draw.rect(self.game.window, [128, 123, 200], [255, 190, 65, 16])
            self.game.window.blit(text, (280, 190))

            text = smallfont.render(self.keys[6], True, [255, 255, 255])
            if 255 <= mouse[0] <= 320 and 220 <= mouse[1] <= 236:
                pygame.draw.rect(self.game.window, [120, 209, 147], [255, 220, 65, 16])
            else:
                pygame.draw.rect(self.game.window, [128, 123, 200], [255, 220, 65, 16])
            self.game.window.blit(text, (280, 220))

            text = smallfont.render(self.keys[7], True, [255, 255, 255])
            if 255 <= mouse[0] <= 320 and 250 <= mouse[1] <= 266:
                pygame.draw.rect(self.game.window, [120, 209, 147], [255, 250, 65, 16])
            else:
                pygame.draw.rect(self.game.window, [128, 123, 200], [255, 250, 65, 16])
            self.game.window.blit(text, (280, 250))

            text = smallfont.render(self.keys[8], True, [255, 255, 255])
            if 255 <= mouse[0] <= 320 and 280 <= mouse[1] <= 296:
                pygame.draw.rect(self.game.window, [120, 209, 147], [255, 280, 65, 16])
            else:
                pygame.draw.rect(self.game.window, [128, 123, 200], [255, 280, 65, 16])
            self.game.window.blit(text, (270, 280))

            text = smallfont.render(self.keys[9], True, [255, 255, 255])
            if 255 <= mouse[0] <= 320 and 310 <= mouse[1] <= 326:
                pygame.draw.rect(self.game.window, [120, 209, 147], [255, 310, 65, 16])
            else:
                pygame.draw.rect(self.game.window, [128, 123, 200], [255, 310, 65, 16])
            self.game.window.blit(text, (280, 310))
            
            text = smallfont.render(self.keys[10], True, [255, 255, 255])
            if 255 <= mouse[0] <= 320 and 340 <= mouse[1] <= 356:
                pygame.draw.rect(self.game.window, [120, 209, 147], [255, 340, 65, 16])
            else:
                pygame.draw.rect(self.game.window, [128, 123, 200], [255, 340, 65, 16])
            self.game.window.blit(text, (280, 340))

            text = smallfont.render(self.keys[11], True, [255, 255, 255])
            if 255 <= mouse[0] <= 320 and 370 <= mouse[1] <= 396:
                pygame.draw.rect(self.game.window, [120, 209, 147], [255, 370, 65, 16])
            else:
                pygame.draw.rect(self.game.window, [128, 123, 200], [255, 370, 65, 16])
            self.game.window.blit(text, (280, 370))
            
            text = smallfont.render(self.keys[12], True, [255, 255, 255])
            if 255 <= mouse[0] <= 330 and 450 <= mouse[1] <= 476:
                pygame.draw.rect(self.game.window, [163, 114, 202], [255, 450, 85, 26])
            else:
                pygame.draw.rect(self.game.window, [182, 134, 135], [255, 450, 85, 26])
            self.game.window.blit(text, (280, 455))
            pygame.display.update()

    def Change_controls(self):
        mouse = pygame.mouse.get_pos()
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                exit()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                prev_state = self.keys.copy()
                if 255 <= mouse[0] <= 320 and 40 <= mouse[1] <= 56:
                    self.keys[0] = self.getKeyPress()
                if 255 <= mouse[0] <= 320 and 70 <= mouse[1] <= 86:
                    self.keys[1] = self.getKeyPress()
                if 255 <= mouse[0] <= 320 and 100 <= mouse[1] <= 116:
                    self.keys[2] = self.getKeyPress()
                if 255 <= mouse[0] <= 320 and 130 <= mouse[1] <= 146:
                    self.keys[3] = self.getKeyPress()
                if 255 <= mouse[0] <= 320 and 160 <= mouse[1] <= 176:
                    self.keys[4] = self.getKeyPress()
                if 255 <= mouse[0] <= 320 and 190 <= mouse[1] <= 206:
                    self.keys[5] = self.getKeyPress()
                if 255 <= mouse[0] <= 320 and 220 <= mouse[1] <= 236:
                    self.keys[6] = self.getKeyPress()
                if 255 <= mouse[0] <= 320 and 250 <= mouse[1] <= 266:
                    self.keys[7] = self.getKeyPress()
                if 255 <= mouse[0] <= 320 and 280 <= mouse[1] <= 296:
                    self.keys[8] = self.getKeyPress()
                if 255 <= mouse[0] <= 320 and 310 <= mouse[1] <= 326:
                    self.keys[9] = self.getKeyPress()
                if 255 <= mouse[0] <= 320 and 340 <= mouse[1] <= 356:
                    self.keys[10] = self.getKeyPress()
                if 255 <= mouse[0] <= 320 and 370 <= mouse[1] <= 386:
                    self.keys[11] = self.getKeyPress()    
                if 255 <= mouse[0] <= 330 and 450 <= mouse[1] <= 476:
                    self.display_menu()
                '''Checks no two functions have same keys'''
                if len(self.keys) != len(set(self.keys)):
                    print('invalid binding')
                    self.keys = prev_state

    @staticmethod
    def getKeyPress():
        while True:
            x = pygame.event.get(pygame.KEYDOWN)
            if len(x) > 0:
                key = x[0].key
                break
        if chr(key).isalpha():
            return chr(key).upper()
        else:
            if key == pygame.K_SPACE:
                return 'Space'
            elif key == pygame.K_LCTRL:
                return 'L-Ctrl'
            elif key == pygame.K_RCTRL:
                return 'R-Ctrl'


class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Credits', 35, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20)
            self.game.draw_text('By team Synergy', 25, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 20)
            self.blit_screen()
