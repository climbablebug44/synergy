import datetime
import traceback
import socket
from CombatSystem.combatGame import combatGame
from common import gameConstants as gc
from Screens.game import Game as gameScreen
import pygame
from TopDownGame.TopDownGame import TopDownGame


def main():
    try:
        pygame.init()
        screen = pygame.display.set_mode(gc.screenSize)
        print(screen.get_size())
        Running = True
        while Running:
            g = gameScreen(screen)
            # TODO: Top Cam Game
            g = TopDownGame(screen)
            g.TopDownGameLoop()
            # TODO: Save previous state of game as CHECKPOINT
            print('running')
            gameInstance = combatGame(gc.screenSize, screen)
            if gameInstance.state:
                print('You won')
                # TODO: CONTINUE GAME WON FROM ENEMY
            else:
                print('You lost')
                Running = False
                # TODO: LOAD LAST CHECKPOINT, LOST FROM ENEMY

    except Exception as ex:
        h = 10
        skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            skt.connect(('localhost', 8081))
            a = traceback.format_exc()
            a = "[" + str(datetime.datetime.now()) + "]\n" + a + "\n\n"
            print(a)
            skt.send(a.encode())
            print(a)
        except ConnectionRefusedError:
            pass
        exit(1)


if __name__ == '__main__':
    main()
