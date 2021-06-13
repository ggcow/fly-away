import random
import time

import pygame.mixer

import parallax
from pygame.locals import (
    K_ESCAPE,
)
from setuptools import glob
import bird
import player
from common import file_path, settings, common_event, MUSIC_VOLUME
from OpenGL.GL import *

music_names = sorted(glob.glob(file_path('music/**')))


def game(best: int):
    pygame.key.set_repeat()
    last_time = time.monotonic_ns()
    start_time = last_time
    delta = 0.
    time_count = 0
    frame_count = 0

    new_best_sound = pygame.mixer.Sound(file_path('win.wav'))
    best_sound_played = False

    background = parallax.Parallax()
    plane = player.Player()
    running = True
    joy_value = pygame.Vector2(0, 0)

    birds = pygame.sprite.Group()

    event_add_bird = pygame.event.custom_type()
    event_more_birds = pygame.event.custom_type()
    event_add_bird_timer = 1000
    pygame.time.set_timer(event_add_bird, event_add_bird_timer)
    pygame.time.set_timer(event_more_birds, 10000)

    pygame.mixer.music.load(random.choice(music_names))
    pygame.mixer.music.set_volume(MUSIC_VOLUME)
    pygame.mixer.music.play(loops=-1, fade_ms=1000)

    while running:
        for event in pygame.event.get():
            common_event(event)
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            elif event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.JOYAXISMOTION:
                if event.axis == 0:
                    joy_value.x = event.value
                elif event.axis == 1:
                    joy_value.y = event.value
            elif event.type == pygame.VIDEORESIZE:
                settings.update_screen(event.w, event.h)
                glViewport(0, 0, settings.current_w, settings.current_h)
                plane.resize()
                b: bird.Bird
                for b in birds:
                    b.resize()

            elif event.type == event_add_bird:
                birds.add(bird.Bird(random.random() * 2 - 1, 0.01))
            elif event.type == event_more_birds:
                event_add_bird_timer *= 0.8
                pygame.time.set_timer(event_add_bird, int(event_add_bird_timer))

        keys = pygame.key.get_pressed()

        background.update(delta, 0, 1, 2, 4, 5)
        plane.update(delta, keys, joy_value)
        birds.update(delta)
        background.update(delta, 3, 6)

        pygame.display.flip()

        for b in birds:
            if pygame.sprite.collide_rect(plane, b):
                if pygame.sprite.collide_mask(plane, b):
                    plane.hp -= 1
                    if plane.hp <= 0:
                        running = False
                        pygame.time.wait(1000)
                    else:
                        birds.remove(b)

        # t = time.monotonic_ns()
        # delta = (t - last_time) / 1_000_000
        # if delta < 50 / 3:
        #     pygame.time.delay(int(50 / 3 - delta))

        t = time.monotonic_ns()
        delta = (t - last_time) / 1_000_000
        last_time = t
        time_count += delta
        frame_count += 1
        if time_count > 1000:
            time_count = 0
            print("FPS : " + str(frame_count))
            frame_count = 0

        if not best_sound_played and (last_time - start_time) / 1_000_000_000 > best:
            new_best_sound.play()
            best_sound_played = True

    return (last_time - start_time) / 1_000_000_000
