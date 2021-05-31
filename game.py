import time
import pygame
import parallax

from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

from common import (
    screen
)


def game():
    last_time = time.monotonic_ns()
    delta = 0
    time_count = 0
    frame_count = 0

    background_parallax = parallax.Parallax()

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            elif event.type == QUIT:
                running = False

        background_parallax.update(delta)
        background_parallax.render()

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
