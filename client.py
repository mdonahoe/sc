"""
client.py
Connect to a world, get the blocks
Print the entire world anytime it changes
if the user makes a change, send to the server
"""
import re
import socket
import sys
import threading

import world

if len(sys.argv) > 1:
    host = sys.argv[1]
else:
    host = ''

username = raw_input('user:')
port = 12345

VALID = re.compile('[A-Za-z0-9]+=-?\d+(\.\d+)?')
def get_user_input():
    """edit blocks"""
    while True:
        x = raw_input('')
        if VALID.match(x):
            world.update(x)
            s.send('update:'+x)
        else:
            print 'bad input'
        world.show()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect((host, port))
s.send('connect:' + username)
a = threading.Thread(target=get_user_input)
a.daemon = True
a.start()

while True:
    data = s.recv(4096)
    cmd, args = data.split(':', 1)
    if cmd == 'world':
        world.reset(args)
    elif cmd == 'update':
        world.update(args)
    else:
        print 'bad server data'
    world.show()
s.close()
