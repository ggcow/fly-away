from common import *
from entities import ressources
from entities import Entity


class Player(Entity):
    deadzone = 0.25
    friction = 0.7

    def __init__(self, level: str):
        Entity.__init__(self, ressources.get(level, 'player'), Vec2(0, 0.5), Vec2(0, 0))
        self.hp = 3
        self.max_speed = 100

    def update(self, delta: float, keys: [POINTER(c_int)], joy_value: Vec2) -> bool:
        if not self.vel_locked:
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

        if Entity.update(self, delta):
            return True

        self.pos.x = min(max(self.pos.x, -1), 1 - self.anim.ratio.x * 2)
        self.pos.y = min(max(self.pos.y, -1), 1 - self.anim.ratio.y * 2)
        self.rect.x = max(min(self.rect.x, settings.current_w), 0)
        self.rect.y = max(min(self.rect.y, settings.current_h), 0)

        return False

