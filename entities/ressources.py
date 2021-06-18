import glob
import random
from common import *
from entities.animation import Animation
from entities.texture import Texture

all_list = []


def load(path, x, y, sprites):
    file_names = glob.glob(file_path(path))
    new_list = []
    for i in range(len(file_names)):
        tex = Texture(file_names[i])
        anim = Animation(tex, sprites, Vec2(x, y))
        new_list.append(anim)
    all_list.append(new_list)


load('sprites/player/*.png', 0.07, 0.07, 1)
load('sprites/bird/*.png', 0.04, 0.05, 6)


def player():
    return random.choice(all_list[0])


def bird():
    return random.choice(all_list[1])


def resize():
    for x in all_list:
        for y in x:
            y.resize()
