import pygame


class spriteSheetManager(object):
    @staticmethod
    def get(filename, colorKey, size, noOfSprites, sizeOut, direction):
        spriteSheet = pygame.transform.scale(pygame.image.load(filename).convert(),
                                             (sizeOut[0] * noOfSprites, sizeOut[1]))
        imageList = []
        for im in range(noOfSprites):
            image = pygame.Surface(sizeOut).convert()
            image.convert_alpha()
            image.set_colorkey(colorKey)
            image.blit(spriteSheet, (-im * sizeOut[0], 0))

            if direction:
                imageList.append(image)
            else:
                imageList.append(pygame.transform.flip(image, True, False))
        return imageList
