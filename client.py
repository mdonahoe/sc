"""
client.py
A simple threaded chat client over UDP
"""

import socket
import sys
import threading

if len(sys.argv) > 1:
    host = sys.argv[1]
else:
    host = ''
port = 12345

def get_user_input():
    while True:
        x = raw_input('')
        print '-'
        s.send(x)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect((host, port))
a = threading.Thread(target=get_user_input)
a.daemon = True
a.start()

while True:
    print s.recv(4096)
s.close()
