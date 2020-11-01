import pygame
from CombatSystem.spriteSheetManager import spriteSheetManager as sSM
from Animation import sprtieDetails as sD

pygame.init()


class animate:

    @staticmethod
    def getSprites(class_name):

        try:
            sprite_class = getattr(sD, class_name)
        except ImportError:
            print(class_name)

        sprites = sSM.getOther(sprite_class.filename, sprite_class.colorKey, sprite_class.sizeIn, sprite_class.noOfSprites, sprite_class.sizeOut, sprite_class.direction)
