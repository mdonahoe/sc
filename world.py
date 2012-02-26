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
BLOCK = ID=float
ID = STRING
FLOAT = A floating point number, duh
"""

# all blocks have a unique id, and a number
BLOCKS = {}
# obviously blocks need more state than this
# but DOUG hasnt gotten a 3D viz working yet

def update(blockstring):
    """converts a block string into a list of block updates"""
    for block in blockstring.split(','):
        name, num = block.split('=')
        BLOCKS[name] = num

def get_all():
    """return all the blocks as a blocklist"""
    return ','.join('%s=%s' % (k,v) for k, v in BLOCKS.iteritems())

def reset(blockstring=None):
    BLOCKS.clear()
    if blockstring:
        update(blockstring)

def show():
    print get_all()
