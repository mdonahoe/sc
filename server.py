"""
server.py

the server maintains the global mapping of blocks, and alerts other clients
of any changes to world blocks.


"""

import socket

import world

host, port = '', 12345
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))

CLIENTS = {}

try:
    while True:
        data, addr = s.recvfrom(100)
        CLIENTS[addr] = data
        print "%s %s" % (addr, data)
        cmd, args = data.split(':', 1)
        if cmd == 'connect':
            CLIENTS[addr] = args
            print '%s connected' % args
            start = 'world:' + world.get_all()
            s.sendto(start, addr)
        elif cmd == 'move':
            world.update_player(args)
            for client in CLIENTS:
                if addr == client: continue
                s.sendto(data, client)
        elif cmd == 'update':
            world.update(args)
            # naively echo to all other clients
            for client in CLIENTS:
                if addr == client: continue
                s.sendto(data, client)
finally:
    print 'Goodbye world'
    s.close()
