"""
server.py
An simple chat server over UDP
"""
import socket

host, port = '', 12345
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))

CLIENTS = {}

try:
    while True:
        data, addr = s.recvfrom(100)
        CLIENTS[addr] = data
        print "%s %s" % (addr, data)
        for client in CLIENTS:
            if addr == client: continue
            s.sendto(data, client)
finally:
    print 'Goodbye world'
    s.close()
