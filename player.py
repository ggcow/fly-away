import collections.abc

import numpy as np
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
from opengl import tex_vao, tex_vbo


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.deadzone = 0.25
        self.friction = 0.7
        self.pos = pygame.Vector2(0, 0.5)
        self.speed = 100
        self.acc = self.speed * 2
        self.vel = pygame.Vector2(0, 0)
        self.image = ressources.player
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.mask = None
        self.w, self.h = 0, 0
        self.image_texture = glGenTextures(1)
        self.resize()
        glBindTexture(GL_TEXTURE_2D, self.image_texture)
        image_data = pygame.image.tostring(self.image, "RGBA", True)
        glTexImage2D(
            GL_TEXTURE_2D, 0, GL_RGBA,
            self.image.get_width(),
            self.image.get_height(),
            0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glBindTexture(GL_TEXTURE_2D, 0)

    def resize(self):
        self.w, self.h = 2 * settings.current_w / 15, 2 * settings.current_h / 15
        self.rect.w, self.rect.h = self.w / 2, self.h / 2
        surf = pygame.transform.scale(self.image, (self.rect.w, self.rect.h))
        self.mask = pygame.mask.from_surface(surf)

    def update(self, delta, keys: collections.abc.Sequence[bool], joy_value: pygame.Vector2):
        if abs(joy_value.x) < self.deadzone and abs(joy_value.y) < self.deadzone:
            joy_value.update(0, 0)

        self.vel.x += joy_value.x * delta
        self.vel.y -= joy_value.y * delta

        if keys[K_UP] or keys[K_DOWN]:
            self.vel.y += (delta, -delta)[keys[K_DOWN]] * (1, 0.707)[keys[K_LEFT] or keys[K_RIGHT]]
        if keys[K_LEFT] or keys[K_RIGHT]:
            self.vel.x += (delta, -delta)[keys[K_LEFT]] * (1, 0.707)[keys[K_UP] or keys[K_DOWN]]

        self.vel *= self.friction ** (delta / 100)

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
        glBindBuffer(GL_ARRAY_BUFFER, tex_vbo)
        vertex_data = np.array([
            self.pos.x, self.pos.y, 0, 0,
            self.pos.x + self.w / settings.current_w, self.pos.y, 1, 0,
            self.pos.x + self.w / settings.current_w, self.pos.y + self.h / settings.current_h, 1, 1,
            self.pos.x, self.pos.y + self.h / settings.current_h, 0, 1
        ], np.float32)
        glBufferData(GL_ARRAY_BUFFER, vertex_data, GL_DYNAMIC_DRAW)
        glBindTexture(GL_TEXTURE_2D, self.image_texture)
        glBindVertexArray(tex_vao)
        glDrawArrays(GL_TRIANGLE_FAN, 0, 4)
        glInvalidateBufferData(tex_vbo)
        glBindTexture(GL_TEXTURE_2D, 0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
