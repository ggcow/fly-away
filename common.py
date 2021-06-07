import os
import sys
from enum import Enum
import pygame

pygame.init()
pygame.display.init()
screen_info = pygame.display.Info()
SCREEN_WIDTH = int(screen_info.current_w / 2)
SCREEN_HEIGHT = int(screen_info.current_h / 2)

MUSIC_VOLUME = 0.1


class Settings:
    def __init__(self):
        self.flags = pygame.DOUBLEBUF | pygame.RESIZABLE
        self.fullscreen = False
        self.muted = False
        self.screen_w = SCREEN_WIDTH
        self.screen_h = SCREEN_HEIGHT
        self.volume = MUSIC_VOLUME

    def toggle_fullscreen(self):
        global screen
        print(screen.get_width(), screen.get_height())
        pygame.event.post(pygame.event.Event(pygame.VIDEORESIZE, {}))
        if self.fullscreen:
            pygame.display.init()
            screen = pygame.display.set_mode((self.screen_w, self.screen_h), self.flags, vsync=1)
        else:
            self.screen_w = screen.get_width()
            self.screen_h = screen.get_height()
            screen = pygame.display.set_mode((screen_info.current_w, screen_info.current_h), self.flags, vsync=1)
        self.fullscreen = not self.fullscreen

    def toggle_mute(self):
        self.muted = not self.muted
        if self.muted:
            self.volume = pygame.mixer.music.get_volume()
            pygame.mixer.music.set_volume(0)
        else:
            pygame.mixer.music.set_volume(self.volume)


settings = Settings()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), settings.flags, vsync=1)

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


def common_event(event: pygame.event.Event):
    if event.type == pygame.KEYDOWN and pygame.key.get_mods() & pygame.KMOD_CTRL:
        if event.key == pygame.K_f:
            settings.toggle_fullscreen()
        elif event.key == pygame.K_s:
            settings.toggle_mute()


class Command(Enum):
    BACK = '!back'
    EXIT = '!exit'
