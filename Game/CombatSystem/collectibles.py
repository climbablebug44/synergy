"""
Contributors: Climbablebug_44
"""

import pygame


class collectibles(pygame.sprite.Sprite):
    def __init__(self, *groups, floor, pos, dire, player):
        super().__init__(groups)
        self.player = player
        self.rect = pygame.rect.Rect(pos[0], pos[1], 10, 10)
        self.floor = floor
        if dire:
            self.velocity = [-10, 0]
        else:
            self.velocity = [10, 0]
        self.image = pygame.transform.scale(pygame.image.load('assets/blank.png'), (10, 10))

    def update(self, *args):
        self.rect = self.rect.move(self.velocity)
        if self.rect.colliderect(self.floor):
            self.velocity[1] = 0
            self.rect.y = self.floor.y - 10
        else:
            self.velocity[1] += 2
        if self.velocity[0] > 0:
            self.velocity[0] -= 1
        elif self.velocity[0] < 0:
            self.velocity[0] += 1
        print(self.rect.y)
        super(collectibles, self).update()


class healthBoost(collectibles):
    def __init__(self, *groups, floor, pos, dire, player):
        super().__init__(*groups, floor=floor, pos=pos, dire=dire, player=player)

    def update(self, *args):
        super(healthBoost, self).update()
        if self.rect.colliderect(self.player):
            self.player.damage(-100)
            print('healed')
            self.kill()
