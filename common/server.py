import socket
import datetime

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('localhost', 8081))
sock.listen(20)

update_file = ['file1.py']
updateAvailable = 'False'

while True:
    try:
        conn, addr = sock.accept()
        data = conn.recv(1024).decode('ascii')
        if data == 'ERROR':
            with open('log.txt', 'a') as f:
                f.write(data)
        elif data == 'UPDATE':
            print('update')
            conn.send(updateAvailable.encode())
            # TODO: SENDING UPDATE FILES
            '''for i in update_file:
                conn.send(i.encode())
                x = conn.recv(1024).decode('ascii')
                with open(i, 'rb') as file:
                    conn.send(file.read())'''

    except KeyboardInterrupt:
        sock.close()
        break
    except Exception as e:
        print(e)
        break
