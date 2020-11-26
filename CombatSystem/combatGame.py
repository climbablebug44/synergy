import pygame
from CombatSystem import playerEntity
from common import gameConstants as c
from CombatSystem.spriteSheetManager import spriteSheetManager
from pygame import mixer


class combatGame(object):
    def __init__(self, size, screen):
        self.clock = pygame.time.Clock()
        # self.sSManager = spriteSheetManager()
        self.screen = screen
        self.size = size
        self.allSprites = pygame.sprite.Group()
        self.platform = pygame.Rect(0, size[1] - 100, size[0], 50)
        self.playingEntities = pygame.sprite.Group()
        self.player = playerEntity.player(self.playingEntities, self.allSprites, platform=self.platform,
                                          time=self.clock)
        self.enemy = playerEntity.EnemyAI(self.playingEntities, self.allSprites, platform=self.platform,
                                          time=self.clock)
        self.enemy2 = playerEntity.smallFlyingEnemySpawner(self.playingEntities, self.allSprites,
                                                           platform=self.platform,
                                                           time=self.clock)
        self.bg = spriteSheetManager.get('assets/bg.png', (0, 0, 0), (2400, 600), 3, (800, 600), True)
        self.running = True
        # Mainloop for combat starts Here: ->
        self.state = self.mainLoop()

    def constructBackground(self):
        """
                Write code for Drawing the background / other stationary sprites
        """
        '''
            For many sprites that have different positions but same image, blitting saves more space and makes more
            sense.
            TODO: blit other background elements
        '''
        self.screen.blit(self.bg[0], (0, 0))

    def pause(self):
        paused = True
        while paused:
            pygame.mixer.music.pause()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        paused = False
                        pygame.mixer.music.unpause()
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
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP or event.type == pygame.MOUSEBUTTONDOWN:
                    self.player.eventHandle(event)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.pause()
                    # TODO: pause
            self.screen.fill(c.color['BLACK'])
            self.constructBackground()  # Draws background
            self.allSprites.update()

            if len(self.player.enemy) != 0:
                pygame.draw.line(self.screen, (255, 0, 0), (
                    self.player.enemy[self.player.lockedEnemy].rect.x,
                    self.player.enemy[self.player.lockedEnemy].rect.y - 10),
                                 (self.player.enemy[self.player.lockedEnemy].rect.x - 10,
                                  self.player.enemy[self.player.lockedEnemy].rect.y - 10))

            self.allSprites.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)

            result = self.checkResult()
            if result is not None:
                return result

    def checkResult(self):
        if len(self.player.enemy) == 0:
            return True
        elif self.player not in self.playingEntities:
            return False
        else:
            return None
