"""
client.py
Connect to a world, get the blocks
Print the entire world anytime it changes
if the user makes a change, send to the server
"""
import socket
import sys
import threading
import time

import world

host = ''
username = ''
port = 12345
c = None

class Connection(object):
    """Manages server connection socket"""
    def __init__(self, username):
        self.username = username
        self.s = self.connect()

    def connect(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((host, port))
        s.send('connect:' + self.username)
        return s

    def send(self, data):
        self.s.send(data)

    def get_data(self):
        while True:
            try:
                data = self.s.recv(4096)
                print 'got: ' + data
                return data
            except socket.error:
                print 'connection refused'
                time.sleep(5)
                print 'done sleeping'
                self.s = self.connect()

def connection(username, terminal=False):
    global c
    c = Connection(username)
    def update_world():
        """sync blocks"""
        while True:
            data = c.get_data()
            cmd, args = data.split(':', 1)
            if cmd == 'world':
                world.reset(args)
            elif cmd == 'update':
                world.update(args)
            elif cmd == 'move':
                world.update_player(args)
            else:
                print 'bad server data'

    a = threading.Thread(target=update_world)
    a.daemon = True
    a.start()

    while terminal:
        x = raw_input('')
        try:
            world.update(x)
            c.send('update:'+x)
        except world.BlockFormatError:
            print 'bad input'
        world.show()

def blockupdate(name, pos):
    # update the world and send to the server
    x = world.make_string(name, pos)
    #world.update(x)
    c.send('update:' + x)

if __name__ == '__main__':
    connection(raw_input('name:'), True)
