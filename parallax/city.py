from parallax import Parallax


class City(Parallax):
    def __init__(self):
        Parallax.__init__(self)

    def gen_height(self, i: int) -> float:
        return (1, 0.2)[i]

    def gen_speed(self, i: int) -> float:
        return (0.5, 2)[i]
