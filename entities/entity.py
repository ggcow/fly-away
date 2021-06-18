import random
import pygame.image
from common import *
from entities.animation import Animation


class Entity(pygame.sprite.Sprite):
    image_source = None
    sprites = 1

    def __init__(self, animations: dict[str: Animation], y: float, speed: float):
        super().__init__()
        self.animations = animations
        anim = animations['fly']
        self.speed = speed
        self.vel = Vec2(-20, 0)
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.pos = Vec2(1, (y * (2 - anim.h / settings.current_h) - anim.h / settings.current_h) / 2)
        self.time = random.random() * 1000
        self.index = 0
        self.anim = anim
        self.mask = anim.mask.masks[self.index]
        self.resize()
        self.state = 'fly'
        self.alive = True

    def resize(self):
        self.rect.w = self.anim.w
        self.rect.h = self.anim.h

    def update(self, delta) -> bool:
        self.time += int(delta)
        if self.time > 1000 and self.state == 'death':
            return True
        self.time %= 1000

        self.pos.x += self.vel.x * delta / 1000 * self.speed
        self.pos.y += self.vel.y * delta / 1000 * self.speed

        self.index = math.floor(self.time / 1000 * self.anim.sprites)
        self.mask = self.anim.mask.masks[self.index]

        self.rect.x = int((1 + self.pos.x) / 2 * settings.current_w)
        self.rect.y = int((1 - self.pos.y) / 2 * settings.current_h) - self.rect.h / 2

    def die(self):
        self.state = 'death'
        self.alive = False
        if self.state in self.animations:
            self.anim = self.animations[self.state]
            self.time = 0

    def render(self):
        self.anim.render(self.pos.x, self.pos.y, self.index)
