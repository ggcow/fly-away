import random
import time
import pygame
import parallax
from setuptools import glob
import bird
import player
from common import *
from OpenGL.GL import *
from timer import Timer

music_names = sorted(glob.glob(file_path('music/**')))


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

    add_bird_timer = Timer(1000)
    more_bird_timer = Timer(10000)

    music = Mix_LoadWAV(file_path(str(random.choice(music_names))))
    Mix_HaltChannel(-1)
    Mix_PlayChannel(-1, music, -1)

    event = SDL_Event()

    while running:

        for i in range(add_bird_timer.update()):
            birds.append(bird.Bird(random.random() * 2 - 1, 0.01))
        for i in range(more_bird_timer.update()):
            add_bird_timer.delay *= 0.8

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
                    plane.resize_masks()
                    for b in birds:
                        b.resize_masks()

        keys = SDL_GetKeyboardState(ctypes.c_int(0))
        background.update(delta, 0, 1, 2, 4, 5)
        plane.update(delta, keys, joy_value)
        plane.render()
        for b in birds:
            if b.update(delta):
                birds.remove(b)
            b.render()
        background.update(delta, 3, 6)

        SDL_GL_SwapWindow(window)

        for b in birds:
            if pygame.sprite.collide_rect(plane, b):
                if pygame.sprite.collide_mask(plane, b):
                    plane.hp -= 1
                    if plane.hp <= 0:
                        running = False
                        pygame.time.wait(1000)
                    else:
                        birds.remove(b)

        if not best_sound_played and time.time() - start_time > best:
            Mix_PlayChannel(-1, new_best_sound, 0)
            best_sound_played = True

    return time.time() - start_time
