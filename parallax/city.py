from parallax import Parallax


class City(Parallax):
    def __init__(self):
        self.path = 'city'
        super().__init__()

    def gen_height(self, i: int) -> float:
        return (1, 0)[i]

    def gen_speed(self, i: int) -> float:
        return (0.5, 2)[i]