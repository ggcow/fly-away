import collections.abc
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
        self.pos = pygame.Vector2(0, common.SCREEN_HEIGHT / 2)
        self.speed = 1
        self.vel = pygame.Vector2(0, 0)
        self.image = pygame.image.load('sprites/plane.png').convert_alpha()
        self.image = pygame.transform.scale(
            self.image, (int(70 * self.image.get_width() / self.image.get_height()), 70))
        self.rect = pygame.rect.Rect(self.pos.x, self.pos.y, self.image.get_width(), self.image.get_height())

    def update(self, delta, keys: collections.abc.Sequence[bool], joy_value: pygame.Vector2):
        if abs(joy_value.x) < self.deadzone and abs(joy_value.y) < self.deadzone:
            joy_value.x = 0
            joy_value.y = 0

        self.vel = joy_value

        if keys[K_UP]:
            self.vel.y -= 1
        if keys[K_DOWN]:
            self.vel.y += 1
        if keys[K_LEFT]:
            self.vel.x -= 1
        if keys[K_RIGHT]:
            self.vel.x += 1
        if self.vel.x == 0 and self.vel.y == 0:
            return
        self.vel.normalize()
        self.pos.x = min(max(self.pos.x + self.vel.x * self.speed * delta, 0), common.SCREEN_WIDTH - self.rect.w)
        self.pos.y = min(max(self.pos.y + self.vel.y * self.speed * delta, 0), common.SCREEN_HEIGHT - self.rect.h)
        self.rect.x = int(self.pos.x)
        self.rect.y = int(self.pos.y)

        # Using keyboard
        if keys[K_UP] or keys[K_DOWN] or keys[K_LEFT] or keys[K_RIGHT]:
            self.vel.x = 0
            self.vel.y = 0

    def render(self):
        common.screen.blit(self.image, self.rect)
