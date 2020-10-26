import pygame
import pickle


# Dictionary is of the form :
# { filename(str) : [colorKey, [height, width], noOfSprites, (sizeX, sizeY)] }
# Using pickle for file Handling to get data about sprite sheets

class spriteSheetManager(object):
    count = 0

    def __init__(self):
        spriteSheetManager.count += 1
        if spriteSheetManager.count >= 2:
            raise Exception('Only one Sprite Sheet Manager can be initialised.')

    @staticmethod
    def get(filename, direction):
        spriteSheet = pygame.image.load(filename).convert()
        with open('CombatSystem/assets/spriteData.pkl', 'rb') as inp:
            spriteDataDict = pickle.load(inp)[filename]
        colorKey = spriteDataDict[0]
        h_w = spriteDataDict[1]
        noOfSprites = spriteDataDict[2]
        size = spriteDataDict[3]
        del spriteDataDict
        imageList = []
        for l in range(noOfSprites):
            image = pygame.Surface(h_w).convert()
            image.convert_alpha()
            image.blit(spriteSheet, (0, 0), (h_w[0] * l, 0, h_w[0], h_w[1]))
            image.set_colorkey(colorKey)
            if direction:
                imageList.append(pygame.transform.scale(image, size))
            else:
                imageList.append(pygame.transform.flip(pygame.transform.scale(image, size), True, False))
        return imageList

    @staticmethod
    def getOther(filename, colorKey, size, noOfSprites, sizeOut, direction):
        spriteSheet = pygame.image.load(filename).convert()
        imageList = []
        for l in range(noOfSprites):
            image = pygame.Surface(size).convert()
            image.convert_alpha()
            image.blit(spriteSheet, (0, 0), (size[0] * l, 0, size[0], size[1]))
            image.set_colorkey(colorKey)
            if direction:
                imageList.append(pygame.transform.scale(image, sizeOut))
            else:
                imageList.append(pygame.transform.flip(pygame.transform.scale(image, sizeOut), True, False))
        return imageList


if __name__ == '__main__':
    spriteData = {
        'playerWalk.png': [(71, 112, 76), [184, 325], 8, (50, 100)]
    }
    with open('../assets/spriteData.pkl', 'wb') as out:
        pickle.dump(spriteData, out, pickle.HIGHEST_PROTOCOL)