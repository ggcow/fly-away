import glob
from common import *
from OpenGL.GL import *
from entities.texture import Texture


class Layer:
    def __init__(self, tex: Texture, speed: float, y: float):
        super().__init__()
        self.w = tex.w
        self.h = tex.h
        self.y = y
        self.speed = speed / 2
        self.scrolling = 0.
        self.tex = tex
        glBindTexture(GL_TEXTURE_2D, tex.id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glBindTexture(GL_TEXTURE_2D, 0)

    def update(self, delta: float):
        self.scrolling += self.speed * delta / 1000 * settings.current_w / self.w / settings.current_h * self.h
        if self.scrolling > 1:
            self.scrolling = 0
        elif self.scrolling < 0:
            self.scrolling = 1
        self.render()

    def render(self):
        portion = settings.current_w * self.h / settings.current_h / self.w
        vertex_data = (c_float * 16)(
            -1, -1, 1, -1, 1, self.y, -1, self.y,
            self.scrolling, 0,
            self.scrolling + portion, 0,
            self.scrolling + portion, 1,
            self.scrolling, 1
        )
        glBufferSubData(GL_ARRAY_BUFFER, 0, 16 * sizeof(c_float), vertex_data)
        glBindTexture(GL_TEXTURE_2D, self.tex.id)
        glDrawArrays(GL_TRIANGLE_FAN, 0, 4)
        glBindTexture(GL_TEXTURE_2D, 0)


class Parallax:
    def __init__(self):
        self.layers: list[Layer] = []
        file_names = sorted(glob.glob(file_path(self.gen_path())))
        for i in range(len(file_names)):
            y, speed = self.gen_height(i), self.gen_speed(i)
            tex = Texture(file_names[i])
            tex.resize(int(tex.w * (y + 1) / 2), tex.h)
            layer = Layer(tex, speed / 8, y)
            layer.scrolling = 0
            self.layers.append(layer)

    def gen_path(self) -> str:
        return 'parallax/*.png'

    def gen_height(self, i: int) -> float:
        return 1

    def gen_speed(self, i: int) -> float:
        return i

    def update(self, delta, *indexes):
        if len(indexes) == 0:
            for layer in self.layers:
                layer.update(delta)
        else:
            for index in indexes:
                if index < len(self.layers):
                    self.layers[index].update(delta)


class Mountains(Parallax):

    def gen_path(self) -> str:
        return 'parallax/mountains/*.png'


class City(Parallax):

    def gen_path(self) -> str:
        return 'parallax/city/*.png'

    def gen_height(self, i: int) -> float:
        return (1, 0)[i]

    def gen_speed(self, i: int) -> float:
        return (0.5, 2)[i]
