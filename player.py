import pygame
import common


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.pos = pygame.Vector2(0, common.SCREEN_HEIGHT / 2)
        self.speed = 1
        self.image = pygame.image.load('sprites/plane.png').convert_alpha()
        self.image = pygame.transform.scale(
            self.image, (int(70 * self.image.get_width() / self.image.get_height()), 70))
        self.rect = pygame.rect.Rect(self.pos.x, self.pos.y, self.image.get_width(), self.image.get_height())

    def update(self, direction: pygame.Vector2):
        if direction.x == 0 and direction.y == 0:
            return
        direction.normalize()
        self.pos.x = min(max(self.pos.x + direction.x * self.speed, 0), common.SCREEN_WIDTH - self.rect.w)
        self.pos.y = min(max(self.pos.y + direction.y * self.speed, 0), common.SCREEN_HEIGHT - self.rect.h)
        self.rect.x = int(self.pos.x)
        self.rect.y = int(self.pos.y)

    def render(self):
        common.screen.blit(self.image, self.rect)
