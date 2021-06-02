import time
import pygame
import parallax

from pygame.locals import (
    K_ESCAPE,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT
)

import player


def game():
    last_time = time.monotonic_ns()
    delta = 0
    time_count = 0
    frame_count = 0

    deadzone = 0.25
    background_parallax = parallax.Parallax()
    plane = player.Player()
    direction = pygame.Vector2(0, 0)
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            elif event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.JOYAXISMOTION:
                if event.axis == 0:
                    direction.x = event.value
                elif event.axis == 1:
                    direction.y = event.value

        keys = pygame.key.get_pressed()

        # Deadzone
        if abs(direction.x) < deadzone and abs(direction.y) < deadzone:
            direction.x = 0
            direction.y = 0

        if keys[K_UP]:
            direction.y -= 1
        if keys[K_DOWN]:
            direction.y += 1
        if keys[K_LEFT]:
            direction.x -= 1
        if keys[K_RIGHT]:
            direction.x += 1

        background_parallax.update(delta)
        plane.update(direction * delta)

        # Using keyboard
        if keys[K_UP] or keys[K_DOWN] or keys[K_LEFT] or keys[K_RIGHT]:
            direction.x = 0
            direction.y = 0

        background_parallax.render()
        plane.render()

        pygame.display.flip()

        t = time.monotonic_ns()
        delta = (t - last_time) / 10_000_000
        last_time = t
        time_count += delta
        frame_count += 1
        if time_count > 100:
            time_count = 0
            print("FPS : " + str(frame_count))
            frame_count = 0
    return 0
