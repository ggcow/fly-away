import collections.abc

import pygame

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT
)

from common import (
    screen
)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.deadzone = 0.25
        self.friction = 0.7
        self.pos = pygame.Vector2(0, 0.5)
        self.speed = 100
        self.acc = self.speed * 2
        self.vel = pygame.Vector2(0, 0)
        self.image_source = pygame.image.load('sprites/plane.png').convert_alpha()
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.mask = None
        self.resize()

    def resize(self):
        self.image = pygame.transform.scale(
            self.image_source, (int(screen.get_width() / 15), int(screen.get_height() / 15)))
        self.rect.w = self.image.get_width()
        self.rect.h = self.image.get_height()
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, delta, keys: collections.abc.Sequence[bool], joy_value: pygame.Vector2):
        if abs(joy_value.x) < self.deadzone and abs(joy_value.y) < self.deadzone:
            joy_value.update(0, 0)

        self.vel += joy_value * delta

        if keys[K_UP] or keys[K_DOWN]:
            self.vel.y += (delta, -delta)[keys[K_UP]] * (1, 0.707)[keys[K_LEFT] or keys[K_RIGHT]]
        if keys[K_LEFT] or keys[K_RIGHT]:
            self.vel.x += (delta, -delta)[keys[K_LEFT]] * (1, 0.707)[keys[K_UP] or keys[K_DOWN]]

        self.vel *= self.friction ** (delta / 100)

        if self.vel.length() > self.speed:
            self.vel *= self.speed / self.vel.length()

        self.pos.x += self.vel.x * delta / 1000 / self.acc
        self.pos.y += self.vel.y * delta / 1000 / self.acc
        self.pos.x = min(max(self.pos.x, 0), 1 - self.image.get_width() / screen.get_width())
        self.pos.y = min(max(self.pos.y, 0), 1 - self.image.get_height() / screen.get_height())

        self.rect.x = int(self.pos.x * screen.get_width())
        self.rect.y = int(self.pos.y * screen.get_height())
        self.render()

    def render(self):
        screen.blit(self.image, self.rect)
