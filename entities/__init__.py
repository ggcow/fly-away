from __future__ import annotations

import math
import random
import time

from common import *
from entities import mask, ressources, animation


class Entity:
    image_source = None
    sprites = 1

    def __init__(self, animations: dict[str: animation.Animation], pos: Vec2, vel: Vec2, flipped: bool = False):
        self.animations = animations
        anim = animations['fly' + ('', '_flipped')[flipped]]
        self.vel = vel
        self.rect = SDL_Rect(0, 0, 0, 0)
        self.pos = Vec2(-1 - anim.ratio.x * 2 if pos.x == -2 else pos.x, pos.y - (anim.ratio.y * (pos.y + 1)))
        self.time = random.random() * 1000
        self.index = 0
        self.anim = anim
        if hasattr(anim, 'mask'):
            self.mask = anim.mask.masks[self.index]
        self.resize()
        self.dead = False
        self.vel_locked = False

        self.test_start_time = time.time()
        self.test_time = self.test_start_time

    def resize(self):
        self.rect.w = self.anim.tex.w
        self.rect.h = self.anim.tex.h

    def update(self, delta, vy_modifier: bool = True) -> bool:
        self.time += int(delta)
        if self.time > 1000 and self.dead:
            return True
        self.time %= 1000

        if vy_modifier:
            t = time.time()
            vx = math.sin(self.test_time - self.test_start_time) - math.sin(t - self.test_start_time)
            self.test_time = t
            self.vel.y += vx * 3

        self.pos.x += self.vel.x * delta / 100000
        self.pos.y += self.vel.y * delta / 100000

        self.index = math.floor(self.time / 1000 * self.anim.sprites)
        if hasattr(self.anim, 'mask'):
            self.mask = self.anim.mask.masks[self.index]

        self.rect.x = round((1 + self.pos.x) * settings.current_w / 2)
        self.rect.y = round((1 - self.pos.y) * settings.current_h / 2) - self.rect.h

        self.anim.render(self.pos.x, self.pos.y, self.index)

    def die(self):
        self.dead = True
        if hasattr(self, 'mask'):
            delattr(self, 'mask')
        self.time = 0
        if 'death' in self.animations:
            self.anim = self.animations['death']
        else:
            self.anim = ressources.get('global', 'explosion')['fly']

    def copy_vel(self, other):
        self.vel = other.vel
        self.vel_locked = True

    def collide(self, other: Entity) -> bool:
        return hasattr(other, 'mask') and hasattr(self, 'mask') and not (
                (self.rect.x >= other.rect.x + other.rect.w)
                or (self.rect.x + self.rect.w <= other.rect.x)
                or (self.rect.y >= other.rect.y + other.rect.h)
                or (self.rect.y + self.rect.h <= other.rect.y)) \
               and mask.collide(self.mask, other.mask, self.rect, other.rect)


from entities.player import Player
from entities.bird import Bird
from entities.hpbar import HpBar
