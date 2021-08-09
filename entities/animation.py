from common import *
from entities import mask
from texture import Texture


class Animation:
    def __init__(self,
                 tex: Texture,
                 sprites: int,
                 format: Vec2,
                 ratio: Vec2,
                 duration: int,
                 mask_needed: bool):
        self.tex = tex
        self.sprites = sprites
        self.format = format
        self.ratio = ratio
        self.w = 2 * self.ratio.x
        self.h = 2 * self.ratio.y
        self.w_tex = 1 / self.format.x
        self.h_tex = 1 / self.format.y
        self.duration = duration
        if mask_needed:
            self.mask = mask.Mask(self)
        self.resize()

    def resize(self):
        self.tex.resize(
            round(settings.current_w * self.ratio.x),
            round(settings.current_h * self.ratio.y)
        )
        if hasattr(self, 'mask'):
            self.mask.resize()

    def render(self, x: float, y: float, index: int):
        x_tex = (index % self.format.x) / self.format.x
        y_tex = (self.format.y - 1 - (index // self.format.x)) / self.format.y

        vertex_data = (ctypes.c_float * 16)(
            x, y,
            x + self.w, y,
            x + self.w, y + self.h,
            x, y + self.h,

            x_tex, y_tex,
            x_tex + self.w_tex, y_tex,
            x_tex + self.w_tex, y_tex + self.h_tex,
            x_tex, y_tex + self.h_tex
        )
        glBufferSubData(GL_ARRAY_BUFFER, 0, 16 * sizeof(c_float), vertex_data)
        glBindTexture(GL_TEXTURE_2D, self.tex.id)
        glDrawArrays(GL_TRIANGLE_FAN, 0, 4)
        glBindTexture(GL_TEXTURE_2D, 0)


