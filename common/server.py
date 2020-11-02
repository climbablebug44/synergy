import socket
import datetime
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('localhost', 8081))
sock.listen(20)
while True:
	try:
		conn, addr = sock.accept()
		data = conn.recv(1024).decode('ascii')
		if data != '':
			with open('log.txt', 'a') as f:
				f.write(data)
	except Exception as e:
		print(e)
