from entities.police import Police
from levels import *


class City(Level):
    def __init__(self):
        self.background = parallax.City()
        Level.__init__(self)
        self.add_police_timer = Timer(1000)

    def update(self, delta, *args):
        for i in range(self.add_police_timer.update(delta)):
            if rand() < 0.5:
                self.flying.append(Police(Vec2(1, rand() * 2 - 1), Vec2(-170 + rand() * 20 - 10, 0)))
            else:
                self.flying.append(Police(Vec2(1, rand() * 2 - 1), Vec2(-20 + rand() * 6 - 3, 0), True))

        return Level.update(self, delta, *args)
