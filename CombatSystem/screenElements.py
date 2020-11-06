import pygame
import common.gameConstants as gc


class levelBar(pygame.sprite.Sprite):
    def __init__(self, *groups, size, position, maxlevel, entity):
        super().__init__(*groups)
        if size[0] < 3 or size[1] < 3:
            raise Exception('Invalid Size')
        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect()
        if position != ():
            self.rect.x, self.rect.y = position
        self.size = size
        self.entity = entity
        self.maxlevel = maxlevel
        self.updatepos = (position == ())

    def update(self):
        self.image.fill(gc.color['BLACK'])
        if self.updatepos:
            self.rect.x, self.rect.y = self.entity.rect.x, self.entity.rect.y


class healthBar(levelBar):
    def __init__(self, *groups, size, position, entity, colors, maxL):
        super().__init__(*groups, position=position, size=size, maxlevel=maxL, entity=entity)
        self.colors = colors

    def update(self):
        super(healthBar, self).update()
        level = (self.entity.health / self.maxlevel) * (self.size[0] - 2)
        pygame.draw.rect(self.image, (self.colors[0] if self.entity.health > 20 else self.colors[1]),
                         pygame.Rect(1, 1, level, self.size[0]))


# TODO: THIS PART IS BROKEN


class stunBar(levelBar):
    def __init__(self, *groups, size, position, maxlevel, entity):
        super().__init__(*groups, size=size, position=position, maxlevel=maxlevel, entity=entity)
        pass


class currentSlot(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        pass
