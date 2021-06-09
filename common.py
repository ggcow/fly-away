import os
import sys
from enum import Enum
import pygame
import opengl

pygame.init()
pygame.display.init()
screen_info = pygame.display.Info()

MUSIC_VOLUME = 0.1
os.environ['SDL_VIDEO_CENTERED'] = '1'
os.environ['SDL_VIDEO_WINDOW_POS'] = '0,0'


class Settings:
    def __init__(self):
        self.flags = pygame.DOUBLEBUF | pygame.RESIZABLE | pygame.OPENGL | pygame.NOFRAME
        self.fullscreen = False
        self.muted = False
        self.initial_width = int(screen_info.current_w / 2)
        self.initial_height = int(screen_info.current_h / 2)
        self.screen_w = self.initial_width
        self.screen_h = self.initial_height
        self.volume = MUSIC_VOLUME
        self.current_w = self.screen_w
        self.current_h = self.screen_h

    def update_screen(self, w: int, h: int):
        global screen
        self.current_w = w
        self.current_h = h
        screen = pygame.display.set_mode((w, h), self.flags, vsync=1)

    def toggle_fullscreen(self):
        if self.fullscreen:
            pygame.display.init()
            pygame.event.post(pygame.event.Event(pygame.VIDEORESIZE, {
                'size': (self.screen_w, self.screen_h),
                'w': self.screen_w, 'h': self.screen_h
            }))
        else:
            self.screen_w = settings.current_w
            self.screen_h = settings.current_h
            pygame.event.post(pygame.event.Event(pygame.VIDEORESIZE, {
                'size': (screen_info.current_w, screen_info.current_h),
                'w': screen_info.current_w, 'h': screen_info.current_h
            }))
        self.fullscreen = not self.fullscreen

    def toggle_mute(self):
        self.muted = not self.muted
        if self.muted:
            self.volume = pygame.mixer.music.get_volume()
            pygame.mixer.music.set_volume(0)
        else:
            pygame.mixer.music.set_volume(self.volume)


settings = Settings()
screen = pygame.display.set_mode((settings.initial_width, settings.initial_height), settings.flags, vsync=1)
opengl.init()

base_path = ''
if getattr(sys, 'frozen', False):
    try:
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
