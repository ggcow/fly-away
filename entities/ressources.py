import glob
from common import *
from entities.animation import Animation
from texture import Texture

dictionary = {}


def load(path: str,
         ratio: Vec2,
         sprites: int = 1,
         sprite_format: Vec2 = Vec2(1, 1),
         duration: int = 1000,
         mask: bool = False,
         flipped: bool = False):

    file_names = glob.glob(file_path(path))
    try:
        level, _, entity, action, _ = path.split('/')
    except ValueError:
        level, _, entity, _ = path.split('/')
        action = 'fly'
    if flipped:
        action += '_flipped'
    if level not in dictionary:
        dictionary[level] = {}
    if entity not in dictionary[level]:
        dictionary[level][entity] = {}
    if action not in dictionary[level][entity]:
        dictionary[level][entity][action] = []
    for i in range(len(file_names)):
        tex = Texture(file_names[i], flipped)
        anim = Animation(tex, sprites, sprite_format, ratio, duration, mask)
        dictionary[level][entity][action].append(anim)


for level_name in ('mountains', 'city', 'forest'):
    load(level_name + '/sprites/player/*.png', Vec2(0.07, 0.07), mask=True)

load('mountains/sprites/bird/fly/*.png', Vec2(0.04, 0.05), 6, Vec2(6, 1), mask=True)
load('mountains/sprites/bird/fly/*.png', Vec2(0.04, 0.05), 6, Vec2(6, 1), mask=True, flipped=True)

load('mountains/sprites/bird/death/*.png', Vec2(0.04, 0.05), 5, Vec2(5, 1), duration=600)
load('mountains/sprites/bird/death/*.png', Vec2(0.04, 0.05), 5, Vec2(5, 1), duration=600, flipped=True)

load('mountains/sprites/bunny/*.png', Vec2(0.04, 0.05), 2, Vec2(2, 1), mask=True, flipped=True)

load('city/sprites/police/*.png', Vec2(0.12, 0.07), mask=True)
load('city/sprites/police/*.png', Vec2(0.12, 0.07), mask=True, flipped=True)

load('city/sprites/truck/*.png', Vec2(0.07, 0.07), mask=True)
load('city/sprites/truck/*.png', Vec2(0.07, 0.07), mask=True, flipped=True)

load('city/sprites/red/*.png', Vec2(0.07, 0.07), mask=True)
load('city/sprites/red/*.png', Vec2(0.07, 0.07), mask=True, flipped=True)

load('global/sprites/explosion/*.png', Vec2(0.08, 0.08), 9, Vec2(3, 3), duration=800)
load('global/sprites/hp/*.png', Vec2(0.02, 0.03))


def get(level: str, item: str):
    return dictionary[level][item]


def resize():
    for level in dictionary.values():
        for entity in level.values():
            for action in entity.values():
                for entry in action:
                    entry.resize()
