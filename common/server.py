import socket
import datetime

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('localhost', 8081))
sock.listen(20)

update_file = ['file1.py']
updateAvailable = 'True'

while True:
    conn, addr = sock.accept()
    try:
        data = conn.recv(1024).decode('ascii')
        if data[:5] == 'ERROR':
            print('[Log Entry]: '+addr[0]+':'+str(addr[1])+' Exception caught')
            with open('log.txt', 'a') as f:
                f.write(data)
        elif data == 'UPDATE':
            print('[Log Entry]: '+addr[0]+':'+str(addr[1])+' Checking/Sending Updates')
            conn.send(updateAvailable.encode())
            conn.send(update_file[0].encode())
            conn.recv(1)
            with open(update_file[0]) as fp:
                conn.send(fp.read().encode())
        conn.close()

    except KeyboardInterrupt:
        conn.close()
        break
    except Exception as e:
        print(e)
        break
