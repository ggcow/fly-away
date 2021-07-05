import random

from levels import *


class Mountains(Level):
    def __init__(self):
        self.background = parallax.Mountains()
        Level.__init__(self)
        self.add_bird_timer = Timer(1000)

    def update(self, delta, *args) -> bool:
        for i in range(self.add_bird_timer.update(delta)):
            self.flying.append(bird.Bird(Vec2(1, random.random() * 2 - 1), Vec2(-20, 0)))

        return Level.update(self, delta, *args)
