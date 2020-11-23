import pygame
from CombatSystem import playerEntity
from common import gameConstants as gc


class projectiles(pygame.sprite.Sprite):
    def __init__(self, *groups, creator):
        super().__init__(*groups)
        self.creator = creator
        self.group = groups[0]
        self.rect = None
        pass

    def update(self, *args):
        if self.rect.x > gc.screenSize[0] or self.rect.x < 0 or self.rect.y < 0 or self.rect.y > gc.screenSize[1]:
            self.kill()


class bullets(projectiles):
    def __init__(self, *groups, creator, vel):
        super().__init__(*groups, creator=creator)
        self.velocity = vel
        self.rect = pygame.Rect(self.creator.rect.x, self.creator.rect.y + 25, 10, 10)
        self.image = pygame.transform.scale(pygame.image.load('assets/blank.png'), (5, 5))
        if vel is None:
            self.kill()

    def update(self, *args):
        self.rect = self.rect.move(self.velocity)
        for i in self.group:
            if self.rect.colliderect(i):
                if (isinstance(i, playerEntity.EnemyAI) and isinstance(self.creator, playerEntity.player)) or (
                        isinstance(i, playerEntity.player) and isinstance(self.creator, playerEntity.EnemyAI)):
                    '''Reducing health'''
                    if not i.blocking or i.stunBar.currLevel() <= 0:
                        i.damage(10, 5)
                    self.kill()
        super(bullets, self).update()


class forceField(projectiles):
    def __init__(self, *groups, creator, direction, pushvel=10, damage=1):
        super().__init__(*groups, creator=creator)
        self.rect = pygame.rect.Rect(self.creator.rect.x, self.creator.rect.y, 1, 100)
        self.image = pygame.transform.scale(pygame.image.load('assets/enemy.png'), (1, 100))
        if direction:
            self.velocity = (30, 0)
        else:
            self.velocity = (-30, 0)
        self.pushvel = pushvel
        self.damage = damage

    def update(self, *args):
        self.rect = self.rect.move(self.velocity)
        for i in self.group:
            if isinstance(i, playerEntity.combatEntity) and i != self.creator and i.rect.colliderect(self.rect):
                if self.velocity[0] > 0:
                    i.velocity[0] = self.pushvel
                else:
                    i.velocity[0] = -self.pushvel
                i.damage(self.damage, 20)
                self.kill()
        super(forceField, self).update()
