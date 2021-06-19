import glob
from common import *
from OpenGL.GL import *


class Layer:
    def __init__(self, surf: SDL_Surface, speed):
        super().__init__()
        self.w = surf.w
        self.h = surf.h
        self.speed = speed / 2
        self.scrolling = 0.
        self.image_texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.image_texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, surf.w, surf.h, 0, GL_RGBA, GL_UNSIGNED_BYTE, c_void_p(surf.pixels))
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glBindTexture(GL_TEXTURE_2D, 0)

    def update(self, delta):
        self.scrolling += self.speed * delta / 1000 * settings.current_w / self.w / settings.current_h * self.h
        if self.scrolling > 1:
            self.scrolling = 0
        elif self.scrolling < 0:
            self.scrolling = 1
        self.render()

    def render(self):
        portion = settings.current_w * self.h / settings.current_h / self.w
        vertex_data = (c_float * 16)(
            -1, -1, 1, -1, 1, 1, -1, 1,
            self.scrolling, 0,
            self.scrolling + portion, 0,
            self.scrolling + portion, 1,
            self.scrolling, 1
        )
        glBufferSubData(GL_ARRAY_BUFFER, 0, 16 * sizeof(c_float), vertex_data)
        glBindTexture(GL_TEXTURE_2D, self.image_texture)
        glDrawArrays(GL_TRIANGLE_FAN, 0, 4)
        glBindTexture(GL_TEXTURE_2D, 0)


class Parallax:
    def __init__(self):
        super().__init__()
        self.w = settings.current_w
        self.layers: list[Layer] = []
        file_names = sorted(glob.glob(file_path('parallax/*.png')))
        for i in range(len(file_names)):
            surf = image.load(file_names[i])
            layer = Layer(surf, i / 8)
            layer.scrolling = 0
            self.layers.append(layer)

    def update(self, delta, *indexes):
        if len(indexes) == 0:
            for layer in self.layers:
                layer.update(delta)
        else:
            for index in indexes:
                self.layers[index].update(delta)
