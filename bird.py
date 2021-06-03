import math

import pygame

from common import (
    screen
)


class Bird(pygame.sprite.Sprite):
    def __init__(self, y: float):
        super().__init__()
        self.speed = 100
        self.sprites = 6
        self.acc = self.speed * 2
        self.vel = pygame.Vector2(-20, 0)
        self.image_source = pygame.image.load('sprites/bird.png').convert_alpha()
        self.image = self.image_source
        self.resize()
        self.pos = pygame.Vector2(1, y)
        self.time = 0
        self.w = self.image.get_width() / self.sprites

    def resize(self):
        self.image = pygame.transform.scale(
            self.image_source,
            (int(screen.get_width() / 18 * self.sprites), int(screen.get_height() / 13)))
        self.w = self.image.get_width() / self.sprites

    def update(self, delta):

        if self.vel.length() > self.speed:
            self.vel *= self.speed / self.vel.length()

        self.pos.x += self.vel.x * delta / 1000 / self.acc
        self.pos.y += self.vel.y * delta / 1000 / self.acc

        if self.pos.x + self.w / self.image.get_width() <= 0:
            self.kill()

        self.time += int(delta)
        self.time %= 1000

        self.render()

    def render(self):
        k = math.floor(self.time / 1000 * self.sprites)
        screen.blit(self.image,
                    (int(self.pos.x * screen.get_width()), int(self.pos.y * screen.get_height())),
                    pygame.Rect(k * self.w, 0, self.w, self.image.get_height()))
