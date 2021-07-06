import random

from entities import ressources
from entities import Entity


class Car(Entity):
    def __init__(self, *args):
        Entity.__init__(self, ressources.get('city', random.choice(('police', 'truck', 'red'))), *args)

    def update(self, delta) -> bool:
        if Entity.update(self, delta) or self.pos.x + self.anim.ratio.x <= -1:
            return True
