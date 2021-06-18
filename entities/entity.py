import random
import pygame.image
from common import *
from entities.animation import Animation


class Entity(pygame.sprite.Sprite):
    image_source = None
    sprites = 1

    def __init__(self, anim: Animation, y: float, speed: float):
        super().__init__()
        self.speed = speed
        self.vel = Vec2(-20, 0)
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.pos = Vec2(1, (y * (2 - anim.h / settings.current_h) - anim.h / settings.current_h) / 2)
        self.time = random.random() * 1000
        self.index = 0
        self.anim = anim
        self.mask = anim.mask.masks[self.index]
        self.resize()

    def resize(self):
        self.rect.w = self.anim.w
        self.rect.h = self.anim.h

    def update(self, delta):
        self.pos.x += self.vel.x * delta / 1000 * self.speed
        self.pos.y += self.vel.y * delta / 1000 * self.speed

        self.time += int(delta)
        self.time %= 1000

        self.index = math.floor(self.time / 1000 * self.anim.sprites)
        self.mask = self.anim.mask.masks[self.index]

        self.rect.x = int((1 + self.pos.x) / 2 * settings.current_w)
        self.rect.y = int((1 - self.pos.y) / 2 * settings.current_h) - self.rect.h / 2

    def render(self):
        self.anim.render(self.pos.x, self.pos.y, self.index)
