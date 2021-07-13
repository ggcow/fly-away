from levels import *
from entities.bunny import Bunny


class Forest(Level):
    def __init__(self):
        self.background = parallax.Forest()
        Level.__init__(self)
        self.add_bird_timer = Timer(1000)
        self.add_bunny_timer = Timer(5000)

    def update(self, delta, *args) -> bool:
        for i in range(self.add_bunny_timer.update(delta)):
            self.flying.append(Bunny(Vec2(rand(), 1.1), Vec2(-20, -30), True))
        for i in range(self.add_bird_timer.update(delta)):
            speed = -20 + rand() * 6 - 3
            flipped = False
            if rand() < 0.5:
                flipped = True
                speed = -170 + rand() * 20 - 10
            self.flying.append(Bird(Vec2(1, rand() * 2 - 1), Vec2(speed, 0), flipped))

        return Level.update(self, delta, *args)
