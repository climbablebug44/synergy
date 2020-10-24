import datetime
import traceback
from Game.CombatSystem.combatGame import combatGame
from Game.CombatSystem import gameConstants as gc
from Game.Screens.game import Game as gameScreen
import pygame

if __name__ == '__main__':
    try:
        pygame.init()
        screen = pygame.display.set_mode(gc.screenSize)
        print(screen.get_size())
        print('Press "Enter" to continue...')
        Running = True
        while Running:
            g = gameScreen(screen)
            print(screen.get_size())
            # TODO: Top Cam Game

            # TODO: Save previous state of game as CHECKPOINT
            gameInstance = combatGame(gc.screenSize, screen)
            if gameInstance.state:
                print('You won')
                # TODO: CONTINUE GAME
            else:
                print('You lost')
                Running = False
                # TODO: LOAD LAST CHECKPOINT

    except Exception as ex:
        a = traceback.format_exc()
        print(a)
        FP = open("CombatSystem/log.txt", "a")
        FP.write("[" + str(datetime.datetime.now()) + "]\n" + a + "\n\n")
        exit(1)
