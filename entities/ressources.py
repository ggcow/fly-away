import glob
import random
from common import *
from entities.animation import Animation
from entities.texture import Texture

dictionary = {}


def load(path: str, x, y, sprites):
    file_names = glob.glob(file_path(path))
    _, entry, action, _ = path.split('/')
    new = False
    if entry not in dictionary:
        dictionary[entry] = []
        new = True
    for i in range(len(file_names)):
        tex = Texture(file_names[i])
        anim = Animation(tex, sprites, Vec2(x, y))
        if new:
            dictionary[entry].append({action: anim})
        else:
            dictionary[entry][i][action] = anim


load('sprites/player/fly/*.png', 0.07, 0.07, 1)
load('sprites/bird/fly/*.png', 0.04, 0.05, 6)
load('sprites/bird/death/*.png', 0.04, 0.05, 5)


def get(item: str):
    return random.choice(dictionary[item])


def resize():
    for value in dictionary.values():
        for entry in value:
            for action in entry.values():
                action.resize()
