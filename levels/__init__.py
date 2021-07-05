import glob

import parallax
from entities import *


class Level:
    plane: Player
    background: parallax.Parallax

    def __init__(self):
        self.name = str(type(self))[str(type(self)).rfind('.')+1:str(type(self)).rfind('\'')].lower()
        self.music = Mix_LoadWAV(random.choice(glob.glob(file_path(os.path.join(self.name, 'music', '**')))))
        self.flying = []
        self.hp_bar = HpBar()
        self.plane = Player(self.name)

    def start(self, hp: int):
        self.plane.hp = hp
        Mix_HaltChannel(-1)
        Mix_PlayChannel(-1, self.music, -1)

    def update(self, delta, keys, joy_value) -> bool:
        self.background.update1(delta)
        if self.plane.update(delta, keys, joy_value):
            return True
        for f in self.flying:
            f: Entity
            if f.update(delta):
                self.flying.remove(f)
        self.background.update2(delta)
        self.hp_bar.update(delta, self.plane.hp)

        SDL_GL_SwapWindow(window)

        for f in self.flying:
            if self.plane.collide(f):
                self.plane.hp -= 1
                if self.plane.hp == 0:
                    self.plane.die()
                    self.plane.copy_vel(f)
                f.die()

        return False

    def resize(self):
        self.plane.resize()
        for f in self.flying:
            f: Entity
            f.resize()
