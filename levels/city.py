from levels import *


class City(Level):
    def __init__(self):
        self.background = parallax.City()
        self.plane = Player('city')
        Level.__init__(self)

    def update(self, *args):
        Level.update(self, *args)

    def resize(self):
        Level.resize(self)
