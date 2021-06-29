from levels import *


class Mountains(Level):
    def __init__(self):
        self.background = parallax.Mountains()
        self.plane = Player('mountains')
        Level.__init__(self)
        self.add_bird_timer = Timer(1000)
        self.more_bird_timer = Timer(10000)

    def update(self, delta, *args):
        for i in range(self.add_bird_timer.update(delta)):
            self.flying.append(bird.Bird(random.random() * 2 - 1, 0.01))
        for i in range(self.more_bird_timer.update(delta)):
            if self.add_bird_timer.delay >= 1.25:
                self.add_bird_timer.delay *= 0.8

        Level.update(self, delta, *args)

    def resize(self):
        Level.resize(self)