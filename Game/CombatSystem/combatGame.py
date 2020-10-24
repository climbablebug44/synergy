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
        # self.allSprites.add(backgroundElements)
        """
            For many sprites that have different positions but same image, blitting saves more space and makes more
            sense.
            TODO: blit other background elements
        """
        grassblock = pygame.transform.scale(pygame.image.load('assets/grass.png'), (80, 80))
        for i in range(20):
            self.screen.blit(grassblock, ((80 * i), c.screenSize[1] - 30))
    def pause(self):
        paused = True
        while paused:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                     
                    if event.key == pygame.K_c:
                        paused = False
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        quit()
        # pygame.display.fill(self.WhITE)
        pygame.draw_text("Paused ",25,435,330)             
        pygame.draw_text("Press c To continue and q to quit",25,435,400)
        pygame.display.update()         

    def mainLoop(self):

        while self.running:
            for event in pygame.event.get():
                # print(type(event))
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP or event.type == pygame.MOUSEBUTTONDOWN:
                    self.player.eventHandle(event)
                if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                    pause()
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
