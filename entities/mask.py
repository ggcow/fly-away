from common import *
import pygame


class Mask:

    def __init__(self, anim):
        self.anim = anim
        self.tex = anim.tex
        buff = (ctypes.c_ubyte * self.tex.image.h * self.tex.image.pitch)()
        memmove(buff, self.tex.image.pixels, sizeof(buff))
        self.image = pygame.image.frombuffer(bytearray(buff), (self.tex.image.w, self.tex.image.h), 'RGBA')
        self.masks = []
        for i in range(self.anim.sprites):
            surf = pygame.Surface((self.tex.w, self.tex.h))
            surf.set_colorkey((0, 0, 0))
            surf.blit(self.image, (0, 0), self.image.get_rect())
            self.masks.append(pygame.mask.from_surface(surf))

    def resize(self):
        for i in range(len(self.masks)):
            self.masks[i] = self.masks[i].scale((self.tex.w, self.tex.h))
