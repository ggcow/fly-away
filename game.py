import random
import time
import pygame
import parallax

from pygame.locals import (
    K_ESCAPE,
)

import bird
import common
import player


def game():
    last_time = time.monotonic_ns()
    delta = 0.
    time_count = 0
    frame_count = 0

    background_parallax = parallax.Parallax()
    plane = player.Player()
    running = True
    joy_value = pygame.Vector2(0, 0)

    birds = pygame.sprite.Group()

    event_add_bird = pygame.event.custom_type()
    event_more_birds = pygame.event.custom_type()
    event_add_bird_timer = 1000
    pygame.time.set_timer(event_add_bird, event_add_bird_timer)
    pygame.time.set_timer(event_more_birds, 10000)

    while running:
        for event in pygame.event.get():
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
                background_parallax.resize()
                plane.resize()
                b: bird.Bird
                for b in birds:
                    b.resize()

            elif event.type == event_add_bird:
                birds.add(bird.Bird(random.random(), 0.01))
            elif event.type == event_more_birds:
                event_add_bird_timer *= 0.8
                pygame.time.set_timer(event_add_bird, int(event_add_bird_timer))

        keys = pygame.key.get_pressed()

        common.screen.fill((0, 0, 0))
        background_parallax.update(delta)
        plane.update(delta, keys, joy_value)
        birds.update(delta)

        pygame.display.flip()

        for b in birds:
            if pygame.sprite.collide_rect(plane, b):
                if pygame.sprite.collide_mask(plane, b):
                    running = False
                    pygame.time.wait(1000)

        # t = time.monotonic_ns()
        # delta = (t - last_time) / 1_000_000
        # if delta < 50 / 3:
        #     pygame.time.wait(int(50 / 3 - delta))

        t = time.monotonic_ns()
        delta = (t - last_time) / 1_000_000
        last_time = t
        time_count += delta
        frame_count += 1
        if time_count > 1000:
            time_count = 0
            print("FPS : " + str(frame_count))
            frame_count = 0
    return 0
