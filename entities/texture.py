from common import *


class Texture:

    def __init__(self, path: str):
        image = IMG_Load(path)
        image = SDL_ConvertSurfaceFormat(image, SDL_PIXELFORMAT_RGBA32, 0)
        self.id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.id)
        surf = image.contents
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, surf.w, surf.h, 0, GL_RGBA, GL_UNSIGNED_BYTE, c_void_p(surf.pixels))
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_BORDER)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_BORDER)
        glBindTexture(GL_TEXTURE_2D, 0)
        self.image = surf
        self.w: int = surf.w
        self.h: int = surf.h

    def resize(self, w: int, h: int):
        self.w = w
        self.h = h
