import datetime
import traceback
from CombatSystem.combatGame import combatGame
from CombatSystem import gameConstants as gc
from Screens.game import Game as gameScreen
import pygame

if __name__ == '__main__':
    try:
        pygame.init()
        screen = pygame.display.set_mode(gc.screenSize)
        print('Press "Enter" to continue...')
        g = gameScreen(screen)
        gameInstance = combatGame(gc.screenSize, screen)

    except Exception as ex:
        a = traceback.format_exc()
        FP = open("CombatSystem/log.txt", "a")
        FP.write("[" + str(datetime.datetime.now()) + "]\n" + a + "\n\n")
        exit(1)
