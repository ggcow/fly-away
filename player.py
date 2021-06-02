import collections.abc
import math

import pygame
import common

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT
)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.deadzone = 0.25
        self.friction = 0.8
        self.pos = pygame.Vector2(0, common.SCREEN_HEIGHT / 2)
        # Smaller acc = faster acceleration
        self.acc = 50
        self.speed = 2 * self.acc
        self.vel = pygame.Vector2(0, 0)
        self.image = pygame.image.load('sprites/plane.png').convert_alpha()
        self.image = pygame.transform.scale(
            self.image, (int(70 * self.image.get_width() / self.image.get_height()), 70))
        self.rect = pygame.rect.Rect(self.pos.x, self.pos.y, self.image.get_width(), self.image.get_height())

    def update(self, delta, keys: collections.abc.Sequence[bool], joy_value: pygame.Vector2):
        if abs(joy_value.x) < self.deadzone and abs(joy_value.y) < self.deadzone:
            joy_value.update(0, 0)

        self.vel += joy_value

        if keys[K_UP]:
            self.vel.y -= (1, 0.707)[keys[K_LEFT] or keys[K_RIGHT]]
        if keys[K_DOWN]:
            self.vel.y += (1, 0.707)[keys[K_LEFT] or keys[K_RIGHT]]
        if keys[K_LEFT]:
            self.vel.x -= (1, 0.707)[keys[K_UP] or keys[K_DOWN]]
        if keys[K_RIGHT]:
            self.vel.x += (1, 0.707)[keys[K_UP] or keys[K_DOWN]]

        self.vel *= self.friction ** (delta / 100)

        if self.vel.length() > self.speed:
            self.vel *= self.speed / self.vel.length()

        if self.vel.length() < self.speed * 0.05 \
                and not (keys[K_UP] or keys[K_DOWN] or keys[K_LEFT] or keys[K_RIGHT] or joy_value.length() > 0):
            self.vel.update(0, 0)
        self.pos.x = min(max(self.pos.x + self.vel.x * delta / self.acc, 0), common.SCREEN_WIDTH - self.rect.w)
        self.pos.y = min(max(self.pos.y + self.vel.y * delta / self.acc, 0), common.SCREEN_HEIGHT - self.rect.h)
        self.rect.x = int(self.pos.x)
        self.rect.y = int(self.pos.y)

    def render(self):
        common.screen.blit(self.image, self.rect)
