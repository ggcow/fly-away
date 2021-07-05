from common import *
from entities import mask, texture


class Animation:
    def __init__(self, tex: texture.Texture, sprites: int, format: Vec2, ratio: Vec2, mask_needed: bool):
        self.tex = tex
        self.sprites = sprites
        self.format = format
        self.ratio = ratio
        self.w = 0
        self.h = 0
        if mask_needed:
            self.mask = mask.Mask(self)
        self.resize()

    def resize(self):
        self.w = settings.current_w * self.ratio.x
        self.h = settings.current_h * self.ratio.y
        self.tex.resize(round(self.w), round(self.h))
        if hasattr(self, 'mask'):
            self.mask.resize()

    def render(self, x: float, y: float, index: int):
        x_tex, y_tex = (index % self.format.x) / self.format.x, (self.format.y - 1 - (index // self.format.x)) / self.format.y
        w_tex, h_tex = 1 / self.format.x, 1 / self.format.y
        w, h = self.w * 2 / settings.current_w, self.h * 2 / settings.current_h

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


