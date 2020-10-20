import pygame
from CombatSystem import gameConstants as c, playerEntity
from CombatSystem.spriteSheetManager import spriteSheetManager


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
        self.mainLoop()

    def constructBackground(self):
        # self.allSprites.add(backgroundElements)
        pass

    def mainLoop(self):

        while self.running:
            for event in pygame.event.get():
                # print(type(event))
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP or event.type == pygame.MOUSEBUTTONDOWN:
                    self.player.eventHandle(event)

            self.screen.fill(c.color['BLACK'])
            self.constructBackground()  # Draws background
            self.allSprites.update()

            '''Drawing Health bars'''
            pygame.draw.rect(self.screen, (0, 255, 0), self.player.healthRect)
            pygame.draw.rect(self.screen, (0, 255, 0), self.enemy.healthRect)
            pygame.draw.rect(self.screen, (255, 0, 0), self.enemy.stunRect)

            self.allSprites.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)
