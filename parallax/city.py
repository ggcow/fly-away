from parallax import Parallax


class City(Parallax):
    def gen_height_from_top(self, i: int) -> float:
        return (1, 0.2)[i]

    def gen_speed(self, i: int) -> float:
        return (0.5, 2)[i]
