import parallax
from entities import *


class Level:
    plane: Player
    background: parallax.Parallax

    def __init__(self):
        self.flying = []

    def update(self, delta, keys, joy_value) -> bool:
        self.background.update(delta, 0, 1, 2, 4, 5)
        if self.plane.update(delta, keys, joy_value):
            return True
        for f in self.flying:
            f: Entity
            if f.update(delta):
                self.flying.remove(f)
        self.background.update(delta, 3, 6)

        SDL_GL_SwapWindow(window)

        for f in self.flying:
            if self.plane.collide(f):
                self.plane.hp -= 1
                if self.plane.hp == 0:
                    self.plane.die()
                    self.plane.copy_vel(f)
                f.die()

    def resize(self):
        self.plane.resize()
        for f in self.flying:
            f: Entity
            f.resize()
