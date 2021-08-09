from entities import ressources
from entities.entity import Entity


class Bird(Entity):
    def __init__(self, *args):
        Entity.__init__(self, ressources.get('mountains', 'bird'), *args)

    def update(self, delta) -> bool:
        if Entity.update(self, delta) or self.pos.x + self.anim.ratio.x * 2 <= -1:
            return True
