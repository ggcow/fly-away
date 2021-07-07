from parallax import Parallax


class Forest(Parallax):
    def __init__(self):
        Parallax.__init__(self)
        self.first_half = (0, 1, 2, 4)

    def gen_height_from_top(self, i: int) -> float:
        return (1, 1, 1, 0.3, 0.1, 0, 0.95, 0.7, -0.3, -0.4)[i]

    def gen_height_from_bottom(self, i: int) -> float:
        return (-1, -1, -1, -0.1, -0.2, 0.6, 0.2, 0, -1, -1)[i]

    def gen_speed(self, i: int) -> float:
        return i - max(0, 0.8*i-3)
