import datetime
import traceback
import socket
from CombatSystem.combatGame import combatGame
from CombatSystem import gameConstants as gc
from Screens.game import Game as gameScreen
import pygame


def main():
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
        h = 10
        skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        skt.connect(('localhost', 8081))
        a = traceback.format_exc()
        a = "[" + str(datetime.datetime.now()) + "]\n" + a + "\n\n"
        skt.send(a.encode())
        print(a)
        exit(1)


if __name__ == '__main__':
    main()
