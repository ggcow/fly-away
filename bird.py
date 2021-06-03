import math
import pygame

from common import (
    screen
)


class Bird(pygame.sprite.Sprite):
    def __init__(self, y: float, speed: float):
        super().__init__()
        self.sprites = 6
        self.speed = speed
        self.vel = pygame.Vector2(-20, 0)
        self.image_source = pygame.image.load('sprites/bird.png').convert_alpha()
        self.image_grid = self.image_source
        self.images = []
        self.masks = []
        self.w = 0
        self.h = 0
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.resize()
        self.pos = pygame.Vector2(1, y)
        self.time = 0
        self.image = self.images[0]
        self.mask = self.masks[0]

    def resize(self):
        self.image_grid = pygame.transform.scale(
            self.image_source,
            (int(screen.get_width() / 18 * self.sprites), int(screen.get_height() / 13)))
        self.w = self.image_grid.get_width() / self.sprites
        self.h = self.image_grid.get_height()
        self.rect.w = self.w
        self.rect.h = self.h
        self.images.clear()
        self.masks.clear()
        for i in range(self.sprites):
            self.images.append(pygame.Surface((self.w, self.image_grid.get_height())))
            self.images[i].set_colorkey((0, 0, 0))
            self.images[i].blit(self.image_grid, (0, 0), pygame.Rect(i * self.w, 0, self.w, self.h))
            self.masks.append(pygame.mask.from_surface(self.images[i]))

    def update(self, delta):
        self.pos.x += self.vel.x * delta / 1000 * self.speed
        self.pos.y += self.vel.y * delta / 1000 * self.speed

        if self.pos.x + self.w / self.image.get_width() <= 0:
            self.kill()

        self.time += int(delta)
        self.time %= 1000

        index = math.floor(self.time / 1000 * self.sprites)
        self.image = self.images[index]
        self.mask = self.masks[index]

        self.rect.x = int(self.pos.x * screen.get_width())
        self.rect.y = int(self.pos.y * screen.get_height())

        self.render()

    def render(self):
        screen.blit(self.image, self.rect)
