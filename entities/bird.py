from entities import ressources
from entities.entity import Entity


class Bird(Entity):

    def __init__(self, *args):
        super().__init__(ressources.bird(), *args)

    def update(self, delta):
        super().update(delta)
        if self.pos.x + self.anim.ratio.x <= -1:
            return 1
