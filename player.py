import math
import numpy

ISQRT2 = 1 / math.sqrt(2)
DEG2RAD = math.pi / 180
cos = lambda x: math.cos(x * DEG2RAD)
sin = lambda x: math.sin(x * DEG2RAD)

class Player(object):
    def __init__(self):
        self.pos = [0, 1.5, 0]
        self.theta = 0
        self.phi = 0
        self.speed = .2

    def update(self, user):
        self.theta -= user.dtheta
        self.phi = max(-90, min(90, self.phi - user.dphi))
        speed = self.speed
        if user.forward and user.sideways:
            speed *= ISQRT2
        forward = [sin(self.theta) * abs(cos(self.phi)),
                -sin(self.phi),
                cos(self.theta) * abs(cos(self.phi))]

        if user.forward:
            self.pos[0] -= speed * user.forward * forward[0]
            self.pos[1] -= speed * user.forward * forward[1]
            self.pos[2] -= speed * user.forward * forward[2]
        sideways = numpy.cross(forward, [0, 1, 0])
        norm = numpy.dot(sideways, sideways)
        speed /= math.sqrt(norm)
        if user.sideways:
            self.pos[0] -= speed * user.sideways * sideways[0]
            self.pos[1] -= speed * user.sideways * sideways[1]
            self.pos[2] -= speed * user.sideways * sideways[2]

