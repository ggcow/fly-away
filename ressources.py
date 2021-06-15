import glob
import random
from common import *


def load(entity: list, path: str):
    file_names = glob.glob(file_path(path))
    for i in range(len(file_names)):
        image = IMG_Load(file_names[i])
        image = SDL_ConvertSurfaceFormat(image, SDL_PIXELFORMAT_RGBA32, 0)
        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        surf = image.contents
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, surf.w, surf.h, 0, GL_RGBA, GL_UNSIGNED_BYTE, c_void_p(surf.pixels))

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_BORDER)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_BORDER)
        glBindTexture(GL_TEXTURE_2D, 0)
        entity.append((surf, texture))


birds = []
players = []

load(birds, 'sprites/bird/*.png')
load(players, 'sprites/player/*.png')


def player():
    return random.choice(players)


def bird():
    return random.choice(birds)
