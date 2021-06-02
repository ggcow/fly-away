import collections.abc

import pygame

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT
)

from common import (
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    screen
)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.deadzone = 0.25
        self.friction = 0.7
        self.pos = pygame.Vector2(0, SCREEN_HEIGHT / 2)
        self.speed = 100
        self.acc = self.speed * 2
        self.vel = pygame.Vector2(0, 0)
        self.image = pygame.image.load('sprites/plane.png').convert_alpha()
        self.image = pygame.transform.scale(
            self.image, (int(SCREEN_WIDTH / 10), int(SCREEN_HEIGHT / 10)))
        self.rect = pygame.rect.Rect(self.pos.x, self.pos.y, self.image.get_width(), self.image.get_height())

    def update(self, delta, keys: collections.abc.Sequence[bool], joy_value: pygame.Vector2):
        if abs(joy_value.x) < self.deadzone and abs(joy_value.y) < self.deadzone:
            joy_value.update(0, 0)

        self.vel += joy_value * delta

        if keys[K_UP]:
            self.vel.y -= delta * (1, 0.707)[keys[K_LEFT] or keys[K_RIGHT]]
        if keys[K_DOWN]:
            self.vel.y += delta * (1, 0.707)[keys[K_LEFT] or keys[K_RIGHT]]
        if keys[K_LEFT]:
            self.vel.x -= delta * (1, 0.707)[keys[K_UP] or keys[K_DOWN]]
        if keys[K_RIGHT]:
            self.vel.x += delta * (1, 0.707)[keys[K_UP] or keys[K_DOWN]]

        self.vel *= self.friction ** (delta / 100)

        if self.vel.length() > self.speed:
            self.vel *= self.speed / self.vel.length()

        # if self.vel.length() < self.speed * 0.05 \
        #         and not (keys[K_UP] or keys[K_DOWN] or keys[K_LEFT] or keys[K_RIGHT] or joy_value.length() > 0):
        #     self.vel.update(0, 0)

        self.pos.x += self.vel.x * delta * SCREEN_WIDTH / 1000 / self.acc
        self.pos.y += self.vel.y * delta * SCREEN_HEIGHT / 1000 / self.acc
        self.pos.x = min(max(self.pos.x, 0), SCREEN_WIDTH - self.rect.w)
        self.pos.y = min(max(self.pos.y, 0), SCREEN_HEIGHT - self.rect.h)
        self.rect.x = int(self.pos.x)
        self.rect.y = int(self.pos.y)

    def render(self):
        screen.blit(self.image, self.rect)
