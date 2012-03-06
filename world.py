"""
world.py
Methods for representing a world.

World 1:

Event types (3 total):
CONNECT
WORLD
UPDATE

Context Free Grammar:
CONNECT = connect:USERNAME
USERNAME = STRING
STRING = [A-Z.,0-9]+
WORLD = world:BLOCKLIST
BLOCKLIST = BLOCK|BLOCKLIST
BLOCK = ID=float,float,float
ID = STRING
FLOAT = A floating point number, duh
"""

import threading

import player
# all blocks have a unique id, and 3-tuple position
BLOCKS = dict(o=(0,0,0),x=(10,0,0),y=(0,10,0),z=(0,0,10))  # a default world
BLOCK_LOCK = threading.Lock()

PLAYERS = dict()  # a list of player objects

class BlockFormatError(Exception): pass

def update_player(playerstring):
    """moves a player"""
    name, nums = playerstring.split('=')
    x,y,z,t,p = [float(n) for n in nums.split(',')]
    if name not in PLAYERS:
        PLAYERS[name] = player.Player()
    PLAYERS[name].pos = [x,y,z]
    PLAYERS[name].theta = t
    PLAYERS[name].phi = p

def get_players():
    PLAYERS['bob'].theta += 1
    return PLAYERS.values()

update_player('bob=0,10,0,45,0')  # this player is always there

def parse(blockstring):
    name, nums = blockstring.split('=')
    values = list(float(x) for x in nums.split(','))
    if len(values) != 3:
        raise BlockFormatError
    return name, values

def update(blockstring):
    """converts a block string into a list of block updates"""
    with BLOCK_LOCK:
        for block in blockstring.split('|'):
            name, values = parse(block)
            BLOCKS[name] = values

def save():
    with open('world.txt', 'w') as f:
        with BLOCK_LOCK:
            for name, pos in BLOCKS.iteritems():
                f.write(make_string(name, pos) + '\n')

def load():
    with open('world.txt', 'r') as f:
        with BLOCK_LOCK:
            BLOCKS.clear()
            for block in f.readlines():
                name, value = parse(block)
                BLOCKS[name] = value
            
def get_all():
    """return all the blocks as a blocklist"""
    blocks = []
    for key, block in BLOCKS.iteritems():
        if len(block) != 3:
            raise BlockFormatError
        x, y, z = block
        blocks.append('%s=%.1f,%.1f,%.1f' % (key, x, y, z))
    return '|'.join(blocks)

def get_list():
    return BLOCKS.values()

def reset(blockstring=None):
    BLOCKS.clear()
    if blockstring:
        update(blockstring)

def make_string(key, pos):
    if len(pos) != 3:
        raise BlockFormatError
    x, y, z = pos
    s = '%s=%.1f,%.1f,%.1f' % (key, x, y, z)
    return s

def make_string_player(name, player):
    x,y,z = player.pos
    s = '%s=%.1f,%.1f,%.1f,%d,%d' % (name, x,y,z,player.theta,player.phi)
    return s

def show():
    print get_all()
