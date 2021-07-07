from entities import ressources
from entities import Entity
from common import *


class HpBar(Entity):
    def __init__(self):
        Entity.__init__(self, ressources.get('global', 'hp'), Vec2(-0.99, 0.99), Vec2(0, 0))

    def update(self, delta: float, hp: int):
        for i in range(hp):
            Entity.update(self, delta, vy_modifier=False)
            self.pos.x += 2 * self.anim.ratio.x + 0.01
        self.pos.x = -0.99
