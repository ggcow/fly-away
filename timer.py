import time


class Timer:
    def __init__(self, delay: float):
        self.delay = float(delay)
        self.clock = time.time()

    def update(self):
        t = time.time()
        delta = (t - self.clock) * 1000
        n = int(delta / self.delay)
        self.clock += self.delay / 1000 * n
        return n
