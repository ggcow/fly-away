import glob
import random
from common import *
from entities.animation import Animation
from entities.texture import Texture

dictionary = {}


def load(path: str, ratio: Vec2, sprites: int, sprite_format: Vec2):
    file_names = glob.glob(file_path(path))
    _, entry, action, _ = path.split('/')
    new = False
    if entry not in dictionary:
        dictionary[entry] = []
        new = True
    for i in range(len(file_names)):
        tex = Texture(file_names[i])
        anim = Animation(tex, sprites, sprite_format, ratio, action == 'fly')
        if len(file_names) == 1 and not new:
            for entity in dictionary[entry]:
                entity[action] = anim
        else:
            if new:
                dictionary[entry].append({action: anim})
            else:
                dictionary[entry][i][action] = anim


load('sprites/player/fly/*.png', Vec2(0.07, 0.07), 1, Vec2(1, 1))
load('sprites/player/death/*.png', Vec2(0.08, 0.08), 9, Vec2(3, 3))
load('sprites/bird/fly/*.png', Vec2(0.04, 0.05), 6, Vec2(6, 1))
load('sprites/bird/death/*.png', Vec2(0.04, 0.05), 5, Vec2(5, 1))


def get(item: str):
    return random.choice(dictionary[item])


def resize():
    for value in dictionary.values():
        for entry in value:
            for action in entry.values():
                action.resize()
