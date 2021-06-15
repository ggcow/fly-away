import ressources
from common import *
from sprite import Sprite


class Player(Sprite):
    deadzone = 0.25
    friction = 0.7
    image_source = ressources.player()[0]

    def __init__(self):
        super().__init__(ressources.player(), 0.5, 1 / 100)
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

        super().update(delta)

        self.pos.x = min(max(self.pos.x, -1), 1 - self.w / settings.current_w)
        self.pos.y = min(max(self.pos.y, -1), 1 - self.h / settings.current_h)

        self.rect.x = int((self.pos.x + 1) / 2 * settings.current_w)
        self.rect.y = int((1 - self.pos.y) / 2 * settings.current_h) - self.size.y
