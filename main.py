import datetime
import traceback
import socket
from CombatSystem.combatGame import combatGame
from common import gameConstants as gc
from Screens.game import Game as gameScreen
import pygame
from TopDownGame.TopDownGame import TopDownGame


def main():
    # TODO: CHECK UPDATE FILES
    skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        skt.connect(('localhost', 8081))
        skt.send('UPDATE'.encode())
        updateAvailable = skt.recv(1024)
        skt.send('True'.encode())
        updateAvailable = updateAvailable.decode('ascii')
        print(updateAvailable)
        if updateAvailable == "True":
            filename = skt.recv(1024)
            skt.send('True'.encode())
            with open(filename, 'wb') as fileRepl:
                x = skt.recv(1024)
                fileRepl.write(x)
        elif updateAvailable == 'False':
            print('no update available')
        else:
            print('Garbage recieved')
    except ConnectionRefusedError:
        print('Server not found')

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
        a = traceback.format_exc()
        a = "[" + str(datetime.datetime.now()) + "]\n" + a + "\n\n"
        skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            skt.connect(('localhost', 8081))
            skt.send(a.encode())
            print(a)
        except ConnectionRefusedError:
            pass
        finally:
            print(a)
            exit(1)


if __name__ == '__main__':
    main()
