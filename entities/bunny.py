from entities import ressources
from entities import Entity


class Bunny(Entity):
    def __init__(self, *args):
        Entity.__init__(self, ressources.get('mountains', 'bunny'), *args)

    def update(self, delta) -> bool:
        if Entity.update(self, delta) or self.pos.x + self.anim.ratio.x * 2 <= -1 or self.pos.y < -1:
            return True
