import os
import sys
from enum import Enum
import pygame

pygame.init()
screen_info = pygame.display.Info()
SCREEN_WIDTH = int(screen_info.current_w / 2)
SCREEN_HEIGHT = int(screen_info.current_h / 2)

MUSIC_VOLUME = 0.4

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)

base_path = ''
if getattr(sys, 'frozen', False):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        print('exc')
        base_path = os.path.abspath(".")


def file_path(relative_path):
    return os.path.join(base_path, 'assets/' + relative_path)


class Command(Enum):
    BACK = '!back'
    EXIT = '!exit'
