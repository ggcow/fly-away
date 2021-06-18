from common import *
from entities import ressources
from entities.entity import Entity


class Player(Entity):
    deadzone = 0.25
    friction = 0.7

    def __init__(self):
        super().__init__(ressources.get('player'), 0.5, 1 / 100)
        self.hp = 3
        self.max_speed = 100

    def update(self, delta: float, keys: [POINTER(c_int)], joy_value: Vec2):
        if abs(joy_value.x) < Player.deadzone and abs(joy_value.y) < Player.deadzone:
            joy_value.x = 0
            joy_value.y = 0

        self.vel.x += joy_value.x * delta
        self.vel.y -= joy_value.y * delta

        if keys[SDL_SCANCODE_UP] or keys[SDL_SCANCODE_DOWN]:
            self.vel.y += (delta, -delta)[keys[SDL_SCANCODE_DOWN]] * \
                          (1, 0.707)[keys[SDL_SCANCODE_LEFT] or keys[SDL_SCANCODE_RIGHT]]
        if keys[SDL_SCANCODE_LEFT] or keys[SDL_SCANCODE_RIGHT]:
            self.vel.x += (delta, -delta)[keys[SDL_SCANCODE_LEFT]] * \
                          (1, 0.707)[keys[SDL_SCANCODE_UP] or keys[SDL_SCANCODE_DOWN]]

        self.vel *= Player.friction ** (delta / 100)

        if self.vel.length() > self.max_speed:
            self.vel *= self.max_speed / self.vel.length()

        self.pos.x = min(max(self.pos.x, -1), 1 - self.anim.ratio.x * 2)
        self.pos.y = min(max(self.pos.y, -1), 1 - self.anim.ratio.y * 2)

        super().update(delta)

