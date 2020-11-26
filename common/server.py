import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('localhost', 8083))
sock.listen(20)

update_file = ['file1.py']
path = ['common/newf/']
updateAvailable = 'False'

while True:
    conn, addr = sock.accept()
    try:
        data = conn.recv(1024).decode('ascii')
        if data[:5] == 'ERROR':
            print('[Log Entry]: ' + addr[0] + ':' + str(addr[1]) + ' Exception caught')
            with open('log.txt', 'a') as f:
                f.write(data)
        elif data == 'UPDATE':
            print('[Log Entry]: ' + addr[0] + ':' + str(addr[1]) + ' Checking/Sending Updates')
            conn.send(updateAvailable.encode())
            if updateAvailable == 'False':
                conn.close()
                continue
            conn.recv(1)
            conn.send((path[0]+update_file[0]).encode())

            with open(update_file[0]) as fp:
                conn.send(fp.read().encode())
        conn.close()

    except KeyboardInterrupt:
        conn.close()
        sock.close()
        break
    except Exception as e:
        print(e)
        break
