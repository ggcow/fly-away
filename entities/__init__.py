from __future__ import annotations

import random
from common import *
from entities import mask, ressources, animation


class Entity:
    image_source = None
    sprites = 1

    def __init__(self, animations: dict[str: animation.Animation], y: float, speed: float):
        self.animations = animations
        anim = animations['fly']
        self.speed = speed
        self.vel = Vec2(-20, 0)
        self.rect = SDL_Rect(0, 0, 0, 0)
        self.pos = Vec2(1, (y * (2 - anim.h / settings.current_h) - anim.h / settings.current_h) / 2)
        self.time = random.random() * 1000
        self.index = 0
        self.anim = anim
        self.mask = anim.mask.masks[self.index]
        self.resize()
        self.state = 'fly'
        self.vel_locked = False

    def resize(self):
        self.rect.w = self.anim.tex.w
        self.rect.h = self.anim.tex.h

    def update(self, delta) -> bool:
        self.time += int(delta)
        if self.time > 1000 and self.state == 'death':
            return True
        self.time %= 1000

        self.pos.x += self.vel.x * delta / 1000 * self.speed
        self.pos.y += self.vel.y * delta / 1000 * self.speed

        self.index = math.floor(self.time / 1000 * self.anim.sprites)
        if self.anim.mask is not None:
            self.mask = self.anim.mask.masks[self.index]

        # self.rect.x = round((1 + self.pos.x) * settings.current_w / 2)
        # self.rect.y = round((1 - self.pos.y - self.anim.ratio.x * 2) * settings.current_h / 2)

        self.rect.x = round((1 + self.pos.x) * settings.current_w / 2)
        self.rect.y = round((1 - self.pos.y) * settings.current_h / 2) - self.rect.h

        self.anim.render(self.pos.x, self.pos.y, self.index)

    def die(self):
        self.state = 'death'
        delattr(self.anim, 'mask')
        self.time = 0
        if self.state in self.animations:
            self.anim = self.animations[self.state]
        else:
            self.anim = ressources.get('global', 'explosion')

    def copy_vel(self, other):
        self.vel = other.vel
        self.vel_locked = True

    def collide(self, other: Entity) -> bool:
        return hasattr(self.anim, 'mask') and not (
                (self.rect.x >= other.rect.x + other.rect.w)
                or (self.rect.x + self.rect.w <= other.rect.x)
                or (self.rect.y >= other.rect.y + other.rect.h)
                or (self.rect.y + self.rect.h <= other.rect.y)) \
               and mask.collide(self.mask, other.mask, self.rect, other.rect)

from entities.player import Player
from entities.bird import Bird