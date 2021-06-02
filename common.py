from enum import Enum

import pygame

pygame.init()
screen_info = pygame.display.Info()
SCREEN_WIDTH = int(screen_info.current_w / 2)
SCREEN_HEIGHT = int(screen_info.current_h / 2)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)


class Command(Enum):
    BACK = '!back'
    EXIT = '!exit'
