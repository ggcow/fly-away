from common import *
from utils import image


class Texture:
    def __init__(self, path: str, flipped: bool = False):
        surf = image.load(path)
        if flipped:
            image.flip(surf)
        self.id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.id)
        glTexImage2D(
            GL_TEXTURE_2D, 0,
            GL_RGBA,
            surf.w, surf.h, 0,
            GL_RGBA, GL_UNSIGNED_BYTE,
            c_void_p(surf.pixels)
        )
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_BORDER)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_BORDER)
        glBindTexture(GL_TEXTURE_2D, 0)
        self.image = surf
        self.w = surf.w
        self.h = surf.h

    def resize(self, w: int, h: int):
        self.w = w
        self.h = h
