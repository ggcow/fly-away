import glob
import pygame
from pygame.sprite import Sprite

from common import (
    screen,
)

direction = 1


class Layer(pygame.sprite.Sprite):
    def __init__(self, group: pygame.sprite.Group, image: pygame.Surface, speed):
        super(Layer, self).__init__(group)
        self.image_source = image
        self.image = image
        self.w = self.image.get_width()
        self.h = self.image.get_height()
        self.resize()
        self.speed = speed
        self.scrolling = 0

    def resize(self):
        self.image = pygame.transform.scale(
            self.image_source,
            (int(screen.get_height() * self.image_source.get_width() / self.image_source.get_height()),
             screen.get_height()))
        surf = pygame.Surface((self.image.get_width() * 4, self.image.get_height()))
        surf.set_colorkey((0, 0, 0))
        surf.blit(self.image, (0, 0))
        surf.blit(self.image, (self.image.get_width(), 0))
        surf.blit(self.image, (self.image.get_width() * 2, 0))
        surf.blit(self.image, (self.image.get_width() * 3, 0))
        surf.convert_alpha()
        self.image = surf
        self.w = self.image.get_width()
        self.h = self.image.get_height()

    def update(self, delta):
        self.scrolling += self.speed * direction * delta * screen.get_width() / self.w / 1000
        if self.scrolling > 1:
            self.scrolling = 0
        elif self.scrolling < 0:
            self.scrolling = 1
        self.render()

    def render(self):
        screen.blit(self.image,
                    (0, 0),
                    pygame.Rect(int(self.scrolling * self.w), 0,
                                screen.get_width(), screen.get_height()))
        if self.w * (1 - self.scrolling) < screen.get_width():
            screen.blit(self.image,
                        pygame.Rect(int(self.w * (1 - self.scrolling)), 0, screen.get_width(), screen.get_height()),
                        pygame.Rect(0, 0, screen.get_width() - int(self.w * (1 - self.scrolling)), self.h))


class Parallax(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.w = screen.get_width()
        file_names = sorted(glob.glob("parallax/*.png"))
        for i in range(len(file_names)):
            image = pygame.image.load(file_names[i]).convert_alpha()
            layer = Layer(self, image, i / 8)
            layer._layer = i - 20
            layer.scrolling = 0

    def resize(self):
        layer: Layer
        for layer in self:
            layer.resize()

