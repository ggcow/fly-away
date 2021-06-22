from ctypes import c_byte, memmove, POINTER
from sdl2 import SDL_ConvertSurfaceFormat, SDL_PIXELFORMAT_RGBA32, SDL_Surface
from sdl2.sdlimage import IMG_Load


def load(path: str) -> SDL_Surface:
    image = IMG_Load(path)
    image = SDL_ConvertSurfaceFormat(image, SDL_PIXELFORMAT_RGBA32, 0).contents
    invert(image)
    return image


def invert(surf: SDL_Surface):
    pitch = surf.pitch
    temp = (c_byte * pitch)()

    for i in range(int(surf.h / 2)):
        row1 = surf.pixels + i * pitch
        row2 = surf.pixels + (surf.h - i - 1) * pitch

        memmove(temp, row1, pitch)
        memmove(row1, row2, pitch)
        memmove(row2, temp, pitch)
