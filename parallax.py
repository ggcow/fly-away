import glob
import pygame

from common import (
    screen,
    SCREEN_HEIGHT,
    SCREEN_WIDTH
)

direction = 1


class Layer(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, speed):
        super(Layer, self).__init__()
        surf = pygame.Surface((image.get_width() * 4, image.get_height()))
        surf.set_colorkey((0, 0, 0))
        surf.blit(image, (0, 0))
        surf.blit(image, (image.get_width(), 0))
        surf.blit(image, (image.get_width() * 2, 0))
        surf.blit(image, (image.get_width() * 3, 0))
        surf.convert_alpha()
        image = surf
        self.speed = speed
        self.image = image
        self.w = image.get_width()
        self.h = image.get_height()
        self.scrolling = 0

    def update(self, delta):
        self.scrolling += self.speed * direction * delta / self.w
        if self.scrolling > 1:
            self.scrolling = 0
        elif self.scrolling < 0:
            self.scrolling = 1

    def render(self):
        screen.blit(self.image,
                    (0, 0),
                    pygame.Rect(int(self.scrolling * self.w), 0,
                                SCREEN_WIDTH, SCREEN_HEIGHT))
        if self.w * (1 - self.scrolling) < SCREEN_WIDTH:
            screen.blit(self.image,
                        pygame.Rect(int(self.w * (1 - self.scrolling)), 0, SCREEN_WIDTH, SCREEN_HEIGHT),
                        pygame.Rect(0, 0, SCREEN_WIDTH - int(self.w * (1 - self.scrolling)), self.h))


class Parallax:
    def __init__(self):
        self.w = SCREEN_WIDTH
        self.layers = []
        file_names = sorted(glob.glob("parallax/*.png"))
        for i in range(len(file_names)):
            image = pygame.image.load(file_names[i]).convert_alpha()
            image = pygame.transform.scale(
                image,
                (int(SCREEN_HEIGHT * image.get_width() / image.get_height()), SCREEN_HEIGHT))
            layer = Layer(image, i / 8)
            layer._layer = i - 20
            layer.scrolling = 0
            self.layers.append(layer)

    def update(self, delta):
        for layer in self.layers:
            layer.update(delta)

    def render(self):
        screen.fill((0, 0, 0))
        for layer in self.layers:
            layer.render()
