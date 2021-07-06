from entities.car import Car
from levels import *


class City(Level):
    def __init__(self):
        self.background = parallax.City()
        Level.__init__(self)
        self.add_police_timer = Timer(1000)

    def update(self, delta, *args):
        for i in range(self.add_police_timer.update(delta)):
            r = rand()
            x = 1
            speed = 20 + rand() * 6 - 3
            flipped = True
            if 3 * r < 1:
                speed = -speed
            elif 3 * r < 2:
                flipped = False
                speed = -170 + rand() * 20 - 10
            else:
                x = -1
            self.flying.append(Car(Vec2(x, rand() * 2 - 1), Vec2(speed, 0), flipped))

        return Level.update(self, delta, *args)
