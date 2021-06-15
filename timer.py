import ctypes
from sdl2 import SDL_Event, SDL_PushEvent
import time


class Timer:
    def __init__(self, event: ctypes.POINTER(SDL_Event), delay: int):
        self.event = event
        self.delay = delay
        self.clock = time.time()

    def update(self):
        t = time.time()
        delta = (t - self.clock) * 1000
        if delta >= self.delay:
            n = int(delta / self.delay)
            self.clock += self.delay / 1000 * n
            for i in range(n):
                SDL_PushEvent(self.event)
