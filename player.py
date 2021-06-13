import collections.abc
from ctypes import c_float

import pygame.image
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT
)
import ressources
from common import *
from OpenGL.GL import *
from opengl import vao, vbo


class Player(pygame.sprite.Sprite):
    deadzone = 0.25
    friction = 0.7

    def __init__(self):
        super().__init__()
        self.pos = pygame.Vector2(0, 0.5)
        self.speed = 100
        self.hp = 3
        self.acc = self.speed * 2
        self.vel = pygame.Vector2(0, 0)
        self.image = ressources.player()
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.mask = None
        self.w, self.h = 0, 0
        self.image, self.texture = ressources.player()
        self.resize()

    def resize(self):
        self.w, self.h = 2 * settings.current_w / 15, 2 * settings.current_h / 15
        self.rect.w, self.rect.h = self.w / 2, self.h / 2
        surf = pygame.transform.scale(self.image, (self.rect.w, self.rect.h))
        self.mask = pygame.mask.from_surface(surf)

    def update(self, delta, keys: collections.abc.Sequence[bool], joy_value: pygame.Vector2):
        if abs(joy_value.x) < Player.deadzone and abs(joy_value.y) < Player.deadzone:
            joy_value.update(0, 0)

        self.vel.x += joy_value.x * delta
        self.vel.y -= joy_value.y * delta

        if keys[K_UP] or keys[K_DOWN]:
            self.vel.y += (delta, -delta)[keys[K_DOWN]] * (1, 0.707)[keys[K_LEFT] or keys[K_RIGHT]]
        if keys[K_LEFT] or keys[K_RIGHT]:
            self.vel.x += (delta, -delta)[keys[K_LEFT]] * (1, 0.707)[keys[K_UP] or keys[K_DOWN]]

        self.vel *= Player.friction ** (delta / 100)

        if self.vel.length() > self.speed:
            self.vel *= self.speed / self.vel.length()

        self.pos.x += self.vel.x * delta / 1000 / self.acc
        self.pos.y += self.vel.y * delta / 1000 / self.acc
        self.pos.x = min(max(self.pos.x, -1), 1 - self.w / settings.current_w)
        self.pos.y = min(max(self.pos.y, -1), 1 - self.h / settings.current_h)

        self.rect.x = int((self.pos.x + 1) / 2 * settings.current_w)
        self.rect.y = int((1 - self.pos.y) / 2 * settings.current_h) - self.rect.h

        self.render()

    def render(self):
        vertex_data = (ctypes.c_float * 16)(
            self.pos.x, self.pos.y,
            self.pos.x + self.w / settings.current_w, self.pos.y,
            self.pos.x + self.w / settings.current_w, self.pos.y + self.h / settings.current_h,
            self.pos.x, self.pos.y + self.h / settings.current_h,
            0, 0, 1, 0, 1, 1, 0, 1
        )
        glBufferSubData(GL_ARRAY_BUFFER, 0, 16 * sizeof(c_float), vertex_data)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glDrawArrays(GL_TRIANGLE_FAN, 0, 4)
        glInvalidateBufferData(vbo)
        glBindTexture(GL_TEXTURE_2D, 0)
