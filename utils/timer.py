class Timer:
    def __init__(self, delay: float):
        self.delay = float(delay)
        self.delta = 0

    def update(self, delta):
        self.delta += delta
        n = int(self.delta / self.delay)
        self.delta -= self.delay * n
        return n
