
class Player(object):
    def __init__(self):
        self.pos = [0, 1.5, 0]
        self.theta = 0
        self.phi = 0

    def update(self, delta):
        dtheta, dphi, dfor = delta
        self.theta += dtheta
        self.phi = max(-90, min(90, self.phi + dphi))
