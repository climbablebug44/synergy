import pygame


class levelBar(pygame.sprite.Sprite):
    def __init__(self, *groups, MaxLevel, entity, pos, size=(710, 20), colorScheme):
        super().__init__(*groups)
        self.maxLevel = MaxLevel
        self.image = pygame.Surface(size).convert()
        self.image.fill((0, 0, 0))
        self.colorScheme = colorScheme
        pygame.draw.rect(self.image, self.colorScheme[1], pygame.rect.Rect(5, 5, self.maxLevel, 10))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos[0], pos[1]  # 40
        self.entity = entity

    def update(self):
        currLevel = self.entity.health
        currLevel = int(700 * (currLevel / self.maxLevel))
        if currLevel > self.maxLevel // 5:
            color = self.colorScheme[1]
        else:
            color = self.colorScheme[0]
        self.image.fill((0, 0, 0))
        pygame.draw.rect(self.image, color, pygame.rect.Rect(5, 5, currLevel, 10))


class currentSlot(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        pass


# TODO: Remove code

'''
if __name__ == '__main__':
    pygame.init()
    c = pygame.time.Clock()
    screen = pygame.display.set_mode((800, 600))
    group = pygame.sprite.Group()
    while True:
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN and e.key == pygame.K_q or e.type == pygame.QUIT:
                exit(0)
        screen.fill((255, 255, 255))
        # blitEntity = healthBar(group)
        group.draw(screen)
        pygame.display.flip()
        c.tick(60)
'''
