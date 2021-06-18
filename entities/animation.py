from common import *
from entities import mask, texture


class Animation:

    def __init__(self, tex: texture.Texture, sprites: int, ratio: Vec2):
        self.tex = tex
        self.sprites: int = sprites
        self.ratio = ratio
        self.w = 0
        self.h = 0
        self.mask = mask.Mask(self)
        self.resize()

    def resize(self):
        self.w = settings.current_w * self.ratio.x * 2
        self.h = settings.current_h * self.ratio.y * 2
        self.tex.resize(int(self.w / 2), int(self.h / 2))
        self.mask.resize()
        
    def render(self, x: float, y: float, index: int):
        vertex_data = (ctypes.c_float * 16)(
            x, y,
            x + self.w / settings.current_w, y,
            x + self.w / settings.current_w, y + self.h / settings.current_h,
            x, y + self.h / settings.current_h,

            index / self.sprites, 0,
            (index + 1) / self.sprites, 0,
            (index + 1) / self.sprites, 1,
            index / self.sprites, 1
        )
        glBufferSubData(GL_ARRAY_BUFFER, 0, 16 * sizeof(c_float), vertex_data)
        glBindTexture(GL_TEXTURE_2D, self.tex.id)
        glDrawArrays(GL_TRIANGLE_FAN, 0, 4)
        glBindTexture(GL_TEXTURE_2D, 0)


