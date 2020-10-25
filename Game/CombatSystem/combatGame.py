import pygame
from Game.CombatSystem import gameConstants as c, playerEntity
from Game.CombatSystem.spriteSheetManager import spriteSheetManager


class combatGame(object):
    def __init__(self, size, screen):
        self.clock = pygame.time.Clock()
        self.sSManager = spriteSheetManager()
        self.screen = screen
        self.size = size
        self.allSprites = pygame.sprite.Group()
        self.platform = pygame.Rect(0, size[1] - 30, size[0], 50)
        self.playingEntities = pygame.sprite.Group()
        self.player = playerEntity.player(self.playingEntities, self.allSprites, ssmanager=self.sSManager,
                                          platform=self.platform, time=self.clock)
        self.enemy = playerEntity.EnemyAI(self.playingEntities, self.allSprites, ssmanager=self.sSManager,
                                          platform=self.platform, time=self.clock)
        self.running = True

        # Mainloop Starts Here: ->
        self.state = self.mainLoop()

    def constructBackground(self):
        """
        Code for Drawing the background
        # bg = self.sSManager.getOther('assets/bg.png(location of asset)', (size of image as tuple (x,y)), 1(number of sprites it has horizontally), (size of out required as tuple(x,y), True(False to flip(mirror image) ))
        # self.screen.blit(bg[0], (0, 0))
        
        """
        '''
            For many sprites that have different positions but same image, blitting saves more space and makes more
            sense.
            TODO: blit other background elements
        '''
        grassblock = pygame.transform.scale(pygame.image.load('assets/grass.png'), (80, 80))
        for i in range(20):
            self.screen.blit(grassblock, ((80 * i), c.screenSize[1] - 30))

    def pause(self):
        print('in pause')
        paused = True
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        paused = False
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        exit()
            self.draw_text("Paused ", 25, 300, 200)
            self.draw_text("Press C To continue and Q to quit", 25, 335, 300)
            pygame.display.flip()

    def draw_text(self, text, size, x, y):
        font = pygame.font.Font('freesansbold.ttf', size)
        text_surface = font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    def mainLoop(self):

        while self.running:
            for event in pygame.event.get():
                # print(type(event))
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP or event.type == pygame.MOUSEBUTTONDOWN:
                    self.player.eventHandle(event)
                if (event.type == pygame.KEYDOWN or event.type == pygame.KEYUP) and event.key == pygame.K_ESCAPE:
                    self.pause()
                    # TODO: pause

            self.screen.fill(c.color['BLACK'])
            self.constructBackground()  # Draws background
            self.allSprites.update()

            '''Drawing Health bars'''
            pygame.draw.rect(self.screen, (0, 255, 0), self.player.healthRect)
            pygame.draw.rect(self.screen, (255, 0, 0), self.enemy.stunRect)

            self.allSprites.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)

            x = self.checkResult()
            if x is not None:
                return x

    def checkResult(self):
        if self.enemy not in self.playingEntities:
            return True
        elif self.player not in self.playingEntities:
            return False
        else:
            return None
