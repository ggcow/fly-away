import ctypes
import random
import time

import sdl2.dll

import parallax
from setuptools import glob
import bird
import player
from common import *
from OpenGL.GL import *
from timer import Timer

music_names = sorted(glob.glob(file_path('music/**')))
EVENT_ADD_BIRD = SDL_RegisterEvents(1)
event_add_bird = SDL_Event()
event_add_bird.user.type = EVENT_ADD_BIRD
event_add_bird.user.code = 0
event_add_bird.user.data1 = 0
event_add_bird.user.data2 = 0



def push_event(x: c_int, event):
    print('LMFAO')
    print(ctypes.cast(event, ctypes.POINTER(SDL_Event)).contents.user.data1)
    SDL_PushEvent(ctypes.cast(event, ctypes.POINTER(SDL_Event)).contents)
    return c_int(1)


def game(best: int):
    start_time = time.time()
    delta = 1000 / 61

    player.Player.resize(1 / 15, 1 / 15)
    bird.Bird.resize(1 / 18, 1 / 14)

    new_best_sound = Mix_LoadWAV(file_path('win.wav'))
    best_sound_played = False

    background = parallax.Parallax()
    plane = player.Player()
    running = True
    joy_value = Vec2(0, 0)

    birds = []
    event_add_bird_delay = 1000
    event_add_bird_timer = Timer(byref(event_add_bird), event_add_bird_delay)

    # pygame.time.set_timer(event_add_bird, event_add_bird_timer)
    # pygame.time.set_timer(event_more_birds, 10000)

    music = Mix_LoadWAV(file_path(str(random.choice(music_names))))
    Mix_HaltChannel(-1)
    Mix_PlayChannel(-1, music, -1)

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
                if event.axis == 0:
                    joy_value.x = event.value
                elif event.axis == 1:
                    joy_value.y = event.value
            elif event.type == SDL_WINDOWEVENT:
                if event.window.event == SDL_WINDOWEVENT_RESIZED:
                    settings.update_screen(event.window.data1, event.window.data2)
                    player.Player.resize(1 / 15, 1 / 15)
                    bird.Bird.resize(1 / 18, 1 / 14)

            elif event.type == EVENT_ADD_BIRD:
                print('new bird')
                birds.append(bird.Bird(random.random() * 2 - 1, 0.01))
            # elif event.type == event_more_birds:
            #     event_add_bird_timer *= 0.8
            #     pygame.time.set_timer(event_add_bird, int(event_add_bird_timer))

        keys = SDL_GetKeyboardState(ctypes.c_int(0))
        background.update(delta, 0, 1, 2, 4, 5)
        plane.update(delta, keys, joy_value)
        plane.render()
        for b in birds:
            if b.update(delta):
                print('bye bird')
                birds.remove(b)
            b.render()
        background.update(delta, 3, 6)

        SDL_GL_SwapWindow(window)

        # for b in birds:
        #     if pygame.sprite.collide_rect(plane, b):
        #         if pygame.sprite.collide_mask(plane, b):
        #             plane.hp -= 1
        #             if plane.hp <= 0:
        #                 running = False
        #                 pygame.time.wait(1000)
        #             else:
        #                 birds.remove(b)

        event_add_bird_timer.update()

        if not best_sound_played and time.time() - start_time > best:
            Mix_PlayChannel(-1, new_best_sound, 0)
            best_sound_played = True

    return time.time() - start_time
