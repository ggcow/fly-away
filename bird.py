import math
import random

import numpy as np

from common import *
import ressources
from OpenGL.GL import *
from opengl import vao, vbo


class Bird(pygame.sprite.Sprite):

    image_source = ressources.bird
    masks = []
    sprites = 6
    w = 0.
    h = 0.
    image_texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, image_texture)
    image_data = pygame.image.tostring(image_source, "RGBA", True)
    glTexImage2D(
        GL_TEXTURE_2D, 0, GL_RGBA,
        image_source.get_width(),
        image_source.get_height(),
        0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_BORDER)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_BORDER)
    glBindTexture(GL_TEXTURE_2D, 0)

    def __init__(self, y: float, speed: float):
        super().__init__()
        self.speed = speed
        self.vel = pygame.Vector2(-20, 0)
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.resize()
        self.pos = pygame.Vector2(1, (y * (2 - Bird.h / settings.current_h) - Bird.h / settings.current_h) / 2)
        self.time = random.random() * 1000
        self.index = 0
        self.mask = Bird.masks[self.index]

    @staticmethod
    def static_resize():
        Bird.w, Bird.h = 2 * settings.current_w / 18, 2 * settings.current_h / 14
        image_grid = pygame.transform.scale(Bird.image_source, (int(Bird.w / 2 * Bird.sprites), int(Bird.h / 2)))
        Bird.masks.clear()
        for i in range(Bird.sprites):
            surf = pygame.Surface((Bird.w / 2, image_grid.get_height()))
            surf.set_colorkey((0, 0, 0))
            surf.blit(image_grid, (0, 0), pygame.Rect(i * Bird.w / 2, 0, Bird.w / 2, Bird.h / 2))
            Bird.masks.append(pygame.mask.from_surface(surf.convert_alpha()))

    def resize(self):
        self.rect.w, self.rect.h = self.w / 2, self.h / 2

    def update(self, delta):
        self.pos.x += self.vel.x * delta / 1000 * self.speed
        self.pos.y += self.vel.y * delta / 1000 * self.speed

        if self.pos.x + self.w / settings.current_w <= -1:
            self.kill()

        self.time += int(delta)
        self.time %= 1000

        self.index = math.floor(self.time / 1000 * Bird.sprites)
        self.mask = Bird.masks[self.index]

        self.rect.x = int((self.pos.x + 1) / 2 * settings.current_w)
        self.rect.y = int((1 - self.pos.y) / 2 * settings.current_h) - self.rect.h

        self.render()

    def render(self):
        vertex_data = np.array([
            self.pos.x, self.pos.y,
            self.index / Bird.sprites, 0,

            self.pos.x + Bird.w / settings.current_w, self.pos.y,
            (self.index + 1) / Bird.sprites, 0,

            self.pos.x + Bird.w / settings.current_w, self.pos.y + Bird.h / settings.current_h,
            (self.index + 1) / Bird.sprites, 1,

            self.pos.x, self.pos.y + Bird.h / settings.current_h,
            self.index / Bird.sprites, 1
        ], np.float32)
        glBufferData(GL_ARRAY_BUFFER, vertex_data, GL_DYNAMIC_DRAW)
        glBindTexture(GL_TEXTURE_2D, Bird.image_texture)
        glDrawArrays(GL_TRIANGLE_FAN, 0, 4)
        glInvalidateBufferData(vbo)
        glBindTexture(GL_TEXTURE_2D, 0)
