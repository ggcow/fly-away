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
    delta = 0
    time_count = 0
    frame_count = 0

    background_parallax = parallax.Parallax()
    plane = player.Player()
    running = True
    joy_value = pygame.Vector2(0, 0)

    birds = pygame.sprite.Group()

    EVENT_ADD_BIRD = pygame.event.custom_type()
    pygame.time.set_timer(EVENT_ADD_BIRD, 1000)

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

            elif event.type == EVENT_ADD_BIRD:
                birds.add(bird.Bird(random.random()))

        keys = pygame.key.get_pressed()

        common.screen.fill((0, 0, 0))
        background_parallax.update(delta)
        plane.update(delta, keys, joy_value)
        birds.update(delta)

        pygame.display.flip()

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
