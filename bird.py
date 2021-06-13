import math
import random
from ctypes import c_float

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

    def __init__(self, y: float, speed: float):
        super().__init__()
        self.speed = speed
        self.vel = pygame.Vector2(-20, 0)
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.image_source, self.texture = ressources.bird()
        self.resize()
        self.pos = pygame.Vector2(1, (y * (2 - Bird.h / settings.current_h) - Bird.h / settings.current_h) / 2)
        self.time = random.random() * 1000
        self.index = 0
        self.mask = Bird.masks[self.index]

    def resize(self):
        Bird.w, Bird.h = 2 * settings.current_w / 18, 2 * settings.current_h / 14
        self.rect.w, self.rect.h = self.w / 2, self.h / 2
        image_grid = pygame.transform.scale(self.image_source, (int(Bird.w / 2 * Bird.sprites), int(Bird.h / 2)))
        Bird.masks.clear()
        for i in range(Bird.sprites):
            surf = pygame.Surface((Bird.w / 2, image_grid.get_height()))
            surf.set_colorkey((0, 0, 0))
            surf.blit(image_grid, (0, 0), pygame.Rect(i * Bird.w / 2, 0, Bird.w / 2, Bird.h / 2))
            Bird.masks.append(pygame.mask.from_surface(surf.convert_alpha()))

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
        vertex_data = (ctypes.c_float * 16)(
            self.pos.x, self.pos.y,
            self.pos.x + Bird.w / settings.current_w, self.pos.y,
            self.pos.x + Bird.w / settings.current_w, self.pos.y + Bird.h / settings.current_h,
            self.pos.x, self.pos.y + Bird.h / settings.current_h,

            self.index / Bird.sprites, 0,
            (self.index + 1) / Bird.sprites, 0,
            (self.index + 1) / Bird.sprites, 1,
            self.index / Bird.sprites, 1
        )
        glBufferSubData(GL_ARRAY_BUFFER, 0, 16 * sizeof(c_float), vertex_data)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glDrawArrays(GL_TRIANGLE_FAN, 0, 4)
        glInvalidateBufferData(vbo)
        glBindTexture(GL_TEXTURE_2D, 0)
