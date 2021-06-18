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

    def resize(self):
        image = pygame.transform.scale(
            self.image, (self.tex.w * self.anim.sprites, self.tex.h))
        self.masks.clear()
        for i in range(self.anim.sprites):
            surf = pygame.Surface((self.tex.w, self.tex.h))
            surf.set_colorkey((0, 0, 0))
            surf.blit(image, (0, 0), pygame.Rect(i * self.tex.w, 0, self.tex.w, self.tex.h))
            self.masks.append(pygame.mask.from_surface(surf))
