import math

class Player(object):
    def __init__(self):
        self.pos = [0, 1.5, 0]
        self.theta = 0
        self.phi = 0
        self.speed = .2

    def update(self, user):
        self.theta -= user.dtheta
        self.phi = max(-90, min(90, self.phi - user.dphi))
        if not user.forward:
            return
        self.pos[0] -= self.speed * (user.forward * math.sin(self.theta * math.pi / 180)
                * abs(math.cos(self.phi * math.pi / 180)))
        self.pos[1] += self.speed * user.forward * math.sin(self.phi * math.pi / 180)
        self.pos[2] -= self.speed * (user.forward * math.cos(self.theta * math.pi / 180)
                * abs(math.cos(self.phi * math.pi / 180)))

