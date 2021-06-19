from common import *
from entities import mask, texture


class Animation:

    def __init__(self, tex: texture.Texture, sprites: int, format: Vec2, ratio: Vec2):
        self.tex = tex
        self.sprites: int = sprites
        self.format = format
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
        x_tex, y_tex = (index % self.format.x) / self.format.x, (self.format.y - 1 - (index // self.format.x)) / self.format.y
        w_tex, h_tex = 1 / self.format.x, 1 / self.format.y
        w, h = self.w / settings.current_w, self.h / settings.current_h

        vertex_data = (ctypes.c_float * 16)(
            x, y,
            x + w, y,
            x + w, y + h,
            x, y + h,

            x_tex, y_tex,
            x_tex + w_tex, y_tex,
            x_tex + w_tex, y_tex + h_tex,
            x_tex, y_tex + h_tex
        )
        glBufferSubData(GL_ARRAY_BUFFER, 0, 16 * sizeof(c_float), vertex_data)
        glBindTexture(GL_TEXTURE_2D, self.tex.id)
        glDrawArrays(GL_TRIANGLE_FAN, 0, 4)
        glBindTexture(GL_TEXTURE_2D, 0)


