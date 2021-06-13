import glob
import random
from OpenGL.GL import *
from common import *


def load(entity: list, path: str):
    file_names = glob.glob(file_path(path))
    for i in range(len(file_names)):
        image = pygame.image.load(file_names[i]).convert_alpha()
        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        image_data = pygame.image.tostring(image, "RGBA", True)
        glTexImage2D(
            GL_TEXTURE_2D, 0, GL_RGBA,
            image.get_width(),
            image.get_height(),
            0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_BORDER)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_BORDER)
        glBindTexture(GL_TEXTURE_2D, 0)
        entity.append((image, texture))


birds = []
players = []

load(birds, 'sprites/bird/*.png')
load(players, 'sprites/player/*.png')


def player():
    return random.choice(players)


def bird():
    return random.choice(birds)
