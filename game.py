import time
import pygame
import parallax

from pygame.locals import (
    K_ESCAPE,
)

import player


def game():
    last_time = time.monotonic_ns()
    delta = 0
    time_count = 0
    frame_count = 0
    clock = pygame.time.Clock()

    background_parallax = parallax.Parallax()
    plane = player.Player()
    running = True
    joy_value = pygame.Vector2(0, 0)

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

        keys = pygame.key.get_pressed()

        background_parallax.update(delta)
        plane.update(delta, keys, joy_value)

        background_parallax.render()
        plane.render()

        pygame.display.flip()

        clock.tick(60)

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
