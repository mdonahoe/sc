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

# all blocks have a unique id, and 3-tuple position
BLOCKS = dict(o=(0,0,0),x=(10,0,0),y=(0,10,0),z=(0,0,10))  # a default world

class BlockFormatError(Exception): pass

def update(blockstring):
    """converts a block string into a list of block updates"""
    for block in blockstring.split('|'):
        name, nums = block.split('=')
        values = list(float(x) for x in nums.split(','))
        if len(values) != 3:
            raise BlockFormatError
        BLOCKS[name] = values

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

def show():
    print get_all()
