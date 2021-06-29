import random
import time
import levels.city
import levels.mountains
from entities import ressources
from common import *
from OpenGL.GL import *


def game(best: int):
    start_time = time.time()
    delta = 1000 / 61

    ressources.resize()

    new_best_sound = Mix_LoadWAV(file_path('win.wav'))
    best_sound_played = False

    level = levels.city.City() if random.random() < 0.5 else levels.mountains.Mountains()
    running = True
    joy_value = Vec2(0, 0)

    event = SDL_Event()

    while running:
        while SDL_PollEvent(byref(event)) > 0:
            common_event(event)

            if event.type == SDL_KEYDOWN:
                if event.key.keysym.sym == SDLK_ESCAPE:
                    running = False
            elif event.type == SDL_QUIT:
                running = False
            elif event.type == SDL_JOYAXISMOTION:
                if event.jaxis.axis == 0:
                    joy_value.x = event.jaxis.value / 32768
                elif event.jaxis.axis == 1:
                    joy_value.y = event.jaxis.value / 32768
            elif event.type == SDL_WINDOWEVENT:
                if event.window.event in (SDL_WINDOWEVENT_RESIZED, SDL_WINDOWEVENT_SIZE_CHANGED):
                    settings.update_screen(event.window.data1, event.window.data2)
                    ressources.resize()
                    level.resize()

        keys = SDL_GetKeyboardState(ctypes.c_int(0))
        if level.update(delta, keys, joy_value):
            break

        if not best_sound_played and time.time() - start_time > best:
            Mix_PlayChannel(-1, new_best_sound, 0)
            best_sound_played = True

    return time.time() - start_time
