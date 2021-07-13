import glob
import random
from common import *
from entities.animation import Animation
from entities.texture import Texture

dictionary = {}


def load(level: str, path: str, ratio: Vec2, sprites: int = 1, sprite_format: Vec2 = Vec2(1, 1), mask: bool = False, flipped: bool = False):
    file_names = glob.glob(file_path(os.path.join(level, path)))
    pack = path.split('/')
    if len(pack) == 4:
        _, entry, action, _ = path.split('/')
    else:
        _, entry, _ = path.split('/')
        action = 'fly'
    if flipped:
        action += '_flipped'
    new_entry = False
    if level not in dictionary:
        dictionary[level] = {}
    if entry not in dictionary[level]:
        dictionary[level][entry] = []
        new_entry = True
    for i in range(len(file_names)):
        tex = Texture(file_names[i], flipped)
        anim = Animation(tex, sprites, sprite_format, ratio, mask)
        if len(file_names) == 1 and not new_entry:
            for entity in dictionary[level][entry]:
                entity[action] = anim
        else:
            if new_entry:
                dictionary[level][entry].append({action: anim})
            else:
                dictionary[level][entry][i][action] = anim


for level_name in ('mountains', 'city', 'forest'):
    load(level_name, 'sprites/player/*.png', Vec2(0.07, 0.07), mask=True)

load('mountains', 'sprites/bird/fly/*.png', Vec2(0.04, 0.05), 6, Vec2(6, 1), mask=True)
load('mountains', 'sprites/bird/death/*.png', Vec2(0.04, 0.05), 5, Vec2(5, 1))
load('mountains', 'sprites/bunny/*.png', Vec2(0.04, 0.05), 2, Vec2(2, 1), mask=True, flipped=True)
load('mountains', 'sprites/bird/fly/*.png', Vec2(0.04, 0.05), 6, Vec2(6, 1), mask=True, flipped=True)
load('mountains', 'sprites/bird/death/*.png', Vec2(0.04, 0.05), 5, Vec2(5, 1), flipped=True)
load('city', 'sprites/police/*.png', Vec2(0.12, 0.07), mask=True)
load('city', 'sprites/police/*.png', Vec2(0.12, 0.07), mask=True, flipped=True)
load('city', 'sprites/truck/*.png', Vec2(0.07, 0.07), mask=True)
load('city', 'sprites/red/*.png', Vec2(0.07, 0.07), mask=True)
load('city', 'sprites/truck/*.png', Vec2(0.07, 0.07), mask=True, flipped=True)
load('city', 'sprites/red/*.png', Vec2(0.07, 0.07), mask=True, flipped=True)
load('global', 'sprites/explosion/*.png', Vec2(0.08, 0.08), 9, Vec2(3, 3))
load('global', 'sprites/hp/*.png', Vec2(0.02, 0.03))


def get(level: str, item: str):
    return random.choice(dictionary[level][item])


def resize():
    for level in dictionary.values():
        for value in level.values():
            for entry in value:
                for action in entry.values():
                    action.resize()
