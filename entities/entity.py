from __future__ import annotations
import random
import time
from common import *
from entities import mask, ressources
from entities.animation import Animation


class Entity:
    def __init__(self,
                 animations: dict[str: list[Animation]],
                 pos: Vec2,
                 vel: Vec2,
                 flipped: bool = False):
        self.animations = animations
        anim = random.choice(animations[('fly', 'fly_flipped')[flipped]])
        self.vel = vel
        self.rect = SDL_Rect(0, 0, 0, 0)
        self.pos = Vec2(
            pos.x - (anim.ratio.x * (pos.x + 1)),
            pos.y - (anim.ratio.y * (pos.y + 1))
        )
        if pos.x < -1:
            self.pos.x = -1 - anim.ratio.x * 2
        elif pos.x > 1:
            self.pos.x = 1
        if pos.y < -1:
            self.pos.y = -1 - anim.ratio.x * 2
        elif pos.y > 1:
            self.pos.y = 1
        self.time = random.random() * anim.duration
        self.index = 0
        self.anim = anim
        if hasattr(anim, 'mask'):
            self.mask = anim.mask.data[self.index]
        self.resize()
        self.dead = False
        self.vy_time = 0

    def resize(self):
        self.rect.w = self.anim.tex.w
        self.rect.h = self.anim.tex.h

    def update(self, delta, vy_modifier: bool = True) -> bool:
        self.time += int(delta)
        if self.time >= self.anim.duration and self.dead:
            return True

        self.time %= self.anim.duration

        self.vy_time += delta / 1000
        vy = (3 + 2 * rand()) * math.sin(self.vy_time) if vy_modifier else 0

        self.pos.x += self.vel.x * delta / 100000
        self.pos.y += (self.vel.y + vy) * delta / 100000

        self.index = math.floor(self.time / self.anim.duration * self.anim.sprites)
        if hasattr(self.anim, 'mask'):
            self.mask = self.anim.mask.data[self.index]

        self.rect.x = round((1 + self.pos.x) * settings.current_w / 2)
        self.rect.y = round((1 - self.pos.y) * settings.current_h / 2) - self.rect.h

        self.anim.render(self.pos.x, self.pos.y, self.index)

    def die(self):
        self.dead = True
        if hasattr(self, 'mask'):
            delattr(self, 'mask')
        self.time = 0
        if 'death' in self.animations:
            self.anim = random.choice(self.animations['death'])
        elif 'death_flipped' in self.animations:
            self.anim = random.choice(self.animations['death'])
        else:
            self.anim = random.choice(ressources.get('global', 'explosion')['fly'])

    def copy_vel(self, other: Entity):
        self.vel = other.vel

    def collide(self, other: Entity) -> bool:
        return hasattr(other, 'mask') and hasattr(self, 'mask') and not (
                (self.rect.x >= other.rect.x + other.rect.w)
                or (self.rect.x + self.rect.w <= other.rect.x)
                or (self.rect.y >= other.rect.y + other.rect.h)
                or (self.rect.y + self.rect.h <= other.rect.y)) \
               and mask.collide(self.mask, other.mask, self.rect, other.rect)
