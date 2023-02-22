import ctypes
import sys
from ctypes import c_byte, memmove, POINTER
from sdl2 import SDL_ConvertSurfaceFormat, SDL_PIXELFORMAT_RGBA32, SDL_Surface
from sdl2.sdlimage import IMG_Load


def load(path: str) -> SDL_Surface:
    return convert_to_rgba32(IMG_Load(path))

def convert_to_rgba32(surf: SDL_Surface) -> SDL_Surface:
    surf = SDL_ConvertSurfaceFormat(surf, SDL_PIXELFORMAT_RGBA32, 0).contents
    invert(surf)
    return surf

def invert(surf: SDL_Surface):
    pitch = surf.pitch
    temp = (c_byte * pitch)()

    for i in range(int(surf.h / 2)):
        row1 = surf.pixels + i * pitch
        row2 = surf.pixels + (surf.h - i - 1) * pitch

        memmove(temp, row1, pitch)
        memmove(row1, row2, pitch)
        memmove(row2, temp, pitch)


def flip(surf: SDL_Surface):
    pitch = surf.pitch
    temp = (c_byte * 4)()
    for i in range(surf.h):
        for j in range(int(surf.w / 2)):
            p1 = surf.pixels + i * pitch + j * 4
            p2 = surf.pixels + (i+1) * pitch - (j+1) * 4
            memmove(temp, p1, 4)
            memmove(p1, p2, 4)
            memmove(p2, temp, 4)
