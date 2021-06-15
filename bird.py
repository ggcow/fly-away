from sprite import Sprite
import ressources
from common import settings


class Bird(Sprite):
    image_source = ressources.bird()[0]
    sprites = 6

    def __init__(self, *args):
        super().__init__(ressources.bird()[1], *args)

    def update(self, delta):
        super().update(delta)
        if self.pos.x + self.w / settings.current_w <= -1:
            return 1
