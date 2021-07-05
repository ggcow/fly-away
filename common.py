import os
import sys
if getattr(sys, 'frozen', False):
    os.chdir(sys._MEIPASS)
    os.environ['PYSDL2_DLL_PATH'] = os.path.join(os.getcwd(), 'dll')
from enum import Enum
import opengl
from sdl2.sdlimage import *
from sdl2.sdlttf import *
from sdl2.sdlmixer import *
from sdl2 import *
from OpenGL.GL import *
from utils import *
from ctypes import *
from random import random as rand


SDL_Init(SDL_INIT_AUDIO | SDL_INIT_VIDEO | SDL_INIT_GAMECONTROLLER)
IMG_Init(IMG_INIT_PNG)
Mix_Init(MIX_INIT_MP3)
TTF_Init()

Mix_OpenAudio(44100, MIX_DEFAULT_FORMAT, 2, 1024)

screen_info = SDL_DisplayMode()
SDL_GetCurrentDisplayMode(0, screen_info)

MUSIC_VOLUME = 10
Mix_Volume(-1, MUSIC_VOLUME)
os.environ['SDL_VIDEO_CENTERED'] = '1'
os.environ['SDL_VIDEO_WINDOW_POS'] = '0,0'


class Settings:
    def __init__(self):
        self.flags = SDL_WINDOW_RESIZABLE | SDL_WINDOW_OPENGL
        self.fullscreen = False
        self.muted = False
        self.initial_width = int(screen_info.w / 2)
        self.initial_height = int(screen_info.h / 2)
        self.current_w = self.initial_width
        self.current_h = self.initial_height
        self.joystick = SDL_NumJoysticks() > 0
        if self.joystick:
            self.joy = SDL_JoystickOpen(0)
            SDL_JoystickEventState(SDL_ENABLE)

    def update_screen(self, w: int, h: int):
        self.current_w = w
        self.current_h = h
        glViewport(0, 0, w, h)

    def toggle_fullscreen(self):
        SDL_SetWindowFullscreen(window, (0, SDL_WINDOW_FULLSCREEN_DESKTOP)[self.fullscreen])
        self.fullscreen = not self.fullscreen

    def toggle_mute(self):
        if self.muted:
            Mix_Volume(-1, MUSIC_VOLUME)
        else:
            Mix_Volume(-1, 0)
        self.muted = not self.muted


settings = Settings()
window = SDL_CreateWindow(b"Game",
                          SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED,
                          settings.initial_width, settings.initial_height, settings.flags)
SDL_GL_SetSwapInterval(1)
context = SDL_GL_CreateContext(window)
SDL_GL_MakeCurrent(window, context)
glViewport(0, 0, settings.initial_width, settings.initial_height)
opengl.init()

try:
    """
    :type sys: sys
    :rtype sys:
    """
    base_path = sys._MEIPASS
except AttributeError:
    base_path = os.path.abspath(".")


def file_path(path):
    return os.path.join('assets', path).encode()


def common_event(event: SDL_Event):
    if event.type == SDL_KEYDOWN and SDL_GetModState() & KMOD_CTRL:
        if event.key.keysym.sym == SDLK_f:
            settings.toggle_fullscreen()
        elif event.key.keysym.sym == SDLK_s:
            settings.toggle_mute()


class Command(Enum):
    BACK = '!back'
    EXIT = '!exit'
    NEXT = '!next'
