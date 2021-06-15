import random

import pygame

from common import *
from pygame import mask
from pygame import Surface
from OpenGL.GL import *


class Sprite:
    image_source = None
    masks = []
    sprites = 1
    w = 0.
    h = 0.
    size = Vec2(0, 0)

    def __init__(self, texture: int, y: float, speed: float):
        self.speed = speed
        self.vel = Vec2(-20, 0)
        self.rect = Vec2(0, 0)
        self.texture = texture
        self.pos = Vec2(1, (y * (2 - type(self).h / settings.current_h) - type(self).h / settings.current_h) / 2)
        self.time = random.random() * 1000
        self.index = 0
        self.surf = None
        # self.mask = Bird.masks[self.index]

    @classmethod
    def resize(cls, x_ratio: float, y_ratio: float):
        cls.w, cls.h = 2 * settings.current_w * x_ratio, 2 * settings.current_h * y_ratio
        cls.size.x, cls.size.y = cls.w / 2, cls.h / 2
        # image_grid = pygame.transform.scale(self.image_source, (int(Bird.w / 2 * Bird.sprites), int(Bird.h / 2)))
        # Bird.masks.clear()
        # for i in range(Bird.sprites):
        #     surf = pygame.Surface((Bird.w / 2, image_grid.get_height()))
        #     surf.set_colorkey((0, 0, 0))
        #     surf.blit(image_grid, (0, 0), pygame.Rect(i * Bird.w / 2, 0, Bird.w / 2, Bird.h / 2))
        #     Bird.masks.append(pygame.mask.from_surface(surf.convert_alpha()))

    def update(self, delta):
        self.pos.x += self.vel.x * delta / 1000 * self.speed
        self.pos.y += self.vel.y * delta / 1000 * self.speed

        self.time += int(delta)
        self.time %= 1000

        self.index = math.floor(self.time / 1000 * type(self).sprites)
        # self.mask = Bird.masks[self.index]

        # self.rect.x = int((self.pos.x + 1) / 2 * settings.current_w)
        # self.rect.y = int((1 - self.pos.y) / 2 * settings.current_h) - self.rect.h

    def render(self):
        vertex_data = (ctypes.c_float * 16)(
            self.pos.x, self.pos.y,
            self.pos.x + type(self).w / settings.current_w, self.pos.y,
            self.pos.x + type(self).w / settings.current_w, self.pos.y + type(self).h / settings.current_h,
            self.pos.x, self.pos.y + type(self).h / settings.current_h,

            self.index / type(self).sprites, 0,
            (self.index + 1) / type(self).sprites, 0,
            (self.index + 1) / type(self).sprites, 1,
            self.index / type(self).sprites, 1
        )
        glBufferSubData(GL_ARRAY_BUFFER, 0, 16 * sizeof(c_float), vertex_data)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glDrawArrays(GL_TRIANGLE_FAN, 0, 4)
        glBindTexture(GL_TEXTURE_2D, 0)
