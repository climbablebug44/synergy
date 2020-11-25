import datetime
import traceback
import socket
from CombatSystem.combatGame import combatGame
from common import gameConstants as gc
from Screens.game import Game as gameScreen
import pygame
from TopDownGame.TopDownGame import TopDownGame


def updateFile(filename, data):
    with open('common/temp/' + filename, 'w+') as fp:
        fp.write(data)


def main():
    # TODO: CHECK UPDATE FILES
    skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        skt.connect(('localhost', 8081))
        skt.send('UPDATE'.encode())
        updateAvailable = skt.recv(1024)
        skt.send('True'.encode())
        updateAvailable = updateAvailable.decode('ascii')

        if updateAvailable == "True":
            print('[GameLog]: Update Available, Updating')
            filename = skt.recv(1024).decode('ascii')
            skt.send(b't')
            data = skt.recv(1024).decode('ascii')
            print(filename, data)
            try:
                while True:
                    data += skt.recv(1024).decode('ascii')
            except ConnectionResetError:
                pass
            updateFile(filename, data)
            print('[GameLog]: Update done')
        elif updateAvailable == 'False':
            print('[GameLog]: No update available, Game already updated')
        else:
            print('[GameLog]: Garbage received')
    except ConnectionRefusedError:
        print('[GameLog]: Server not found')
    finally:
        skt.close()

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
            skt.send(b'ERROR')
            skt.send(a.encode())
            print('Error report sent')
        except ConnectionRefusedError:
            pass
        finally:
            exit(1)


if __name__ == '__main__':
    main()
