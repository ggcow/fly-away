import math


class Vec2:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, other):
        if isinstance(other, Vec2):
            self.x += other.x
            self.y += other.y
        else:
            self.x += other
            self.y += other
        return self

    def __sub__(self, other):
        if isinstance(other, Vec2):
            self.x -= other.x
            self.y -= other.y
        else:
            self.x -= other
            self.y -= other
        return self

    def __mul__(self, other):
        if isinstance(other, Vec2):
            return self.x * other.x + self.y * other.y
        else:
            self.x *= other
            self.y *= other
            return self

    def __truediv__(self, other):
        self.x /= other
        self.y /= other
        return self

    def length(self):
        return math.hypot(self.x, self.y)

    def normalized(self):
        length = self.length()
        if not length:
            length = 1.0
        self.x /= length
        self.y /= length
        return self

    def limited(self, maxlength=1.0):
        length = self.length()
        if length > maxlength:
            self.x *= maxlength / length
            self.y *= maxlength / length
        return self
