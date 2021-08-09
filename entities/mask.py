from common import *


class Mask:
    def __init__(self, anim):
        self.anim = anim
        self.tex = anim.tex
        self.data = []
        self.source_masks = []
        surf = anim.tex.image
        alpha = cast(surf.pixels, POINTER(c_ubyte))[3:surf.h * surf.pitch:4]
        self.w, self.h = int(surf.w / anim.format.x), int(surf.h / anim.format.y)
        for i in range(self.anim.sprites):
            x, y = i % anim.format.x, anim.format.y - 1 - (i // anim.format.x)
            mask = []
            for j in reversed(range(y * self.h, (y + 1) * self.h)):
                mask += alpha[j * surf.w + x * self.w:j * surf.w + (x + 1) * self.w]
            self.source_masks.append(mask)
            # for y in range(self.h):
            #     for x in range(self.w):
            #         print('..' if mask[y * self.w + x] == 0 else 'XX', end='')
            #     print()
            # print()
        for m in self.source_masks:
            self.data.append(m.copy())

    def resize(self):
        self.scale(self.tex.w, self.tex.h)

    def scale(self, w: int, h: int):
        self.data.clear()
        for mask in self.source_masks:
            new_mask = []
            ny = dny = 0
            dy = h
            for y in range(self.h):
                while dny < dy:
                    nx = dnx = 0
                    dx = w
                    for x in range(self.w):
                        while dnx < dx:
                            new_mask.append(mask[y * self.w + x])
                            nx += 1
                            dnx += self.w
                        dx += w
                    ny += 1
                    dny += self.h
                dy += h
            self.data.append(new_mask)
            # for y in range(h):
            #     for x in range(w):
            #         print('XX' if new_mask[y * w + x] > 0 else '..', end='')
            #     print()
            # print()


def collide(mask_a, mask_b, rect_a: SDL_Rect, rect_b: SDL_Rect) -> bool:
    x1, y1 = max(rect_a.x, rect_b.x), max(rect_a.y, rect_b.y)
    x2, y2 = min(rect_a.x + rect_a.w, rect_b.x + rect_b.w), min(rect_a.y + rect_a.h, rect_b.y + rect_b.h)
    w, h = x2 - x1, y2 - y1
    start_a_x, start_a_y = x1 - rect_a.x, y1 - rect_a.y
    start_b_x, start_b_y = x1 - rect_b.x, y1 - rect_b.y
    # print(rect_a.x, rect_a.y, rect_a.w, rect_a.h)
    # print(rect_b.x, rect_b.y, rect_b.w, rect_b.h)
    # for y in range(rect_b.h):
    #     for x in range(rect_b.w):
    #         print('XX' if mask_b[y * rect_b.w + x] > 0 else '..', end='')
    #     print()
    # print()
    # print('w h', w, h)
    # print('start_a', start_a_x, start_a_y)
    # print('start_b', start_b_x, start_b_y)
    # for y in range(h):
    #     for x in range(w):
    #         a = mask_a[(start_a_y + y) * rect_a.w + x + start_a_x] > 0
    #         b = mask_b[(start_b_y + y) * rect_b.w + x + start_b_x] > 0
    #         print(('..', 'AA', 'BB', 'XX')
    #               [a | b << 1]
    #               , end='')
    #     print()
    # print()

    # xx1, yy1 = min(rect_a.x, rect_b.x), min(rect_a.y, rect_b.y)
    # xx2, yy2 = max(rect_a.x + rect_a.w, rect_b.x + rect_b.w), max(rect_a.y + rect_a.h, rect_b.y + rect_b.h)
    # ww, hh = xx2 - xx1, yy2 - yy1
    # start_a_xx, start_a_yy = rect_a.x - xx1, rect_a.y - yy1
    # start_b_xx, start_b_yy = rect_b.x - xx1, rect_b.y - yy1
    # for y in range(hh):
    #     for x in range(ww):
    #         if start_a_xx <= x < start_a_xx + rect_a.w and start_a_yy <= y < start_a_yy + rect_a.h:
    #             a = mask_a[(y - start_a_yy) * rect_a.w + x - start_a_xx] > 0
    #         else:
    #             a = False
    #         if start_b_xx <= x < start_b_xx + rect_b.w and start_b_yy <= y < start_b_yy + rect_b.h:
    #             b = mask_b[(y - start_b_yy) * rect_b.w + x - start_b_xx] > 0
    #         else:
    #             b = False
    #         print(('..', 'AA', 'BB', 'XX')[a | b << 1], end='')
    #     print()
    # print()

    for y in range(h):
        for x in range(w):
            if mask_a[(start_a_y + y) * rect_a.w + x + start_a_x] == 255\
                    and mask_b[(start_b_y + y) * rect_b.w + x + start_b_x] == 255:
                return True
    return False
