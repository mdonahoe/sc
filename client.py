import socket
host = 'toqbot.com'
port = '12345'
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect((host, port))
s.send('hello world')
print s.recv(100)  # fixed
s.close()
