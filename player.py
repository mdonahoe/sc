import math
import numpy

ISQRT2 = 1 / math.sqrt(2)

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
        forward = [math.sin(self.theta * math.pi / 180) * abs(math.cos(self.phi * math.pi / 180)),
                -math.sin(self.phi * math.pi / 180),
                math.cos(self.theta * math.pi / 180) * abs(math.cos(self.phi * math.pi / 180))]

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

