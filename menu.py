import time
from ctypes import c_float

import pygame.time
from OpenGL.GL import *
from pygame.locals import (
    K_ESCAPE,
    K_DOWN,
    K_UP,
    K_RETURN,
    K_KP_ENTER,
    K_BACKSPACE,
    KMOD_SHIFT,
    KMOD_CTRL,
    KMOD_ALT
)
from common import *
from opengl import vao, vbo

font = pygame.font.Font(file_path('menu_font.ttf'), 30)

image_texture = glGenTextures(1)


class Menu:
    class Action(Enum):
        BACK = 1
        ENTER = 2
        QUIT = 3
        UP = 4
        DOWN = 5
        DELETE = 6
        UNICODE = 7

    def __init__(self):
        self.deadzone = 0.7
        self.JOYSTICK_DELAY = 0.130
        self.joy_delay = self.JOYSTICK_DELAY
        self.time = time.monotonic()
        self.unicode = []

    def poll_events(self) -> list[Action]:
        self.unicode.clear()
        t = time.monotonic()
        self.joy_delay = max(0., self.joy_delay - t + self.time)
        self.time = t
        last_joy_value = 1
        actions = []
        for event in pygame.event.get():
            common_event(event)

            keydown = event.type == pygame.KEYDOWN
            joy_axis_motion = pygame.joystick.get_init() and event.type == pygame.JOYAXISMOTION
            joy_button_down = pygame.joystick.get_init() and event.type == pygame.JOYBUTTONDOWN

            if (keydown and event.key == K_ESCAPE) or (joy_button_down and event.button == 1):
                actions.append(Menu.Action.BACK)
            elif (keydown and event.key == K_BACKSPACE) or (joy_button_down and event.button == 2):
                actions.append(Menu.Action.DELETE)
            elif keydown and event.key == K_DOWN or \
                    joy_axis_motion and event.axis == 1 and event.value > self.deadzone and self.joy_delay == 0 \
                    and abs(event.value) > last_joy_value:
                actions.append(Menu.Action.DOWN)
                if joy_axis_motion:
                    self.joy_delay = self.JOYSTICK_DELAY
            elif keydown and event.key == K_UP or \
                    joy_axis_motion and event.axis == 1 and event.value < -self.deadzone and self.joy_delay == 0 \
                    and abs(event.value) > last_joy_value:
                actions.append(Menu.Action.UP)
                if joy_axis_motion:
                    self.joy_delay = self.JOYSTICK_DELAY
            elif keydown and event.key in (K_RETURN, K_KP_ENTER) or joy_button_down and event.button == 0:
                actions.append(Menu.Action.ENTER)
            elif event.type == pygame.QUIT:
                actions.append(Menu.Action.QUIT)
            elif event.type == pygame.VIDEORESIZE:
                settings.update_screen(event.w, event.h)
                glViewport(0, 0, settings.current_w, settings.current_h)
            elif keydown and not pygame.key.get_mods() & (KMOD_SHIFT | KMOD_CTRL | KMOD_ALT):
                actions.append(Menu.Action.UNICODE)
                self.unicode.append(event.unicode)

            if event.type == pygame.JOYAXISMOTION and event.axis == 1:
                last_joy_value = abs(event.value) + 0.1
        return actions

    def main(self, info: dict):
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        pygame.key.set_repeat(500, 70)
        player_name = info['player_name']
        pygame.font.init()
        position = 0
        clock = pygame.time.Clock()
        options = ('Start', 'High scores', 'Credits', 'Exit')
        pygame.mixer.music.load(file_path('menu.mp3'))
        pygame.mixer.music.set_volume(MUSIC_VOLUME / 2)
        pygame.mixer.music.play(-1, fade_ms=100)
        n = len(options)
        while True:
            for event in self.poll_events():
                if event == Menu.Action.QUIT:
                    return Command.EXIT
                if event == Menu.Action.ENTER:
                    if position == options.index('Start'):
                        player_name = self.name(player_name if not isinstance(player_name, Command) else '')
                        if player_name != Command.BACK:
                            return player_name
                    elif position == options.index('High scores'):
                        if self.high_scores(info['scores']) == Command.EXIT:
                            return Command.EXIT
                    elif position == options.index('Credits'):
                        if self.credits() == Command.EXIT:
                            return Command.EXIT
                        pygame.mixer.music.load(file_path('menu.mp3'))
                        pygame.mixer.music.set_volume(MUSIC_VOLUME / 2)
                        pygame.mixer.music.play(-1, fade_ms=100)
                    elif position == options.index('Exit'):
                        return Command.EXIT
                if event == Menu.Action.DOWN:
                    position = min(position + 1, n - 1)
                if event == Menu.Action.UP:
                    position = max(position - 1, 0)

            glClear(GL_COLOR_BUFFER_BIT)

            for i in range(n):
                text = ('→ ' + options[i] + ' ←', options[i])[i != position]
                text_surf = font.render(text, False, (255, 255, 255))
                w = text_surf.get_width() / settings.current_w * 2
                x = - w / 2
                h = text_surf.get_height() / settings.current_h * 2
                y = h + (20 + text_surf.get_height()) * (n / 2 - i) / settings.current_h * 2

                blit(x, y, w, h, text_surf)

            if info['player_score'] > 0:
                text = 'New best for ' + \
                       info['player_name'] + \
                       ' : ' if info['player_score'] == info['scores'][info['player_name']] else ''
                text_surf = font.render(text + str(round(info['player_score'], 2)), False, (255, 255, 255))
                w = text_surf.get_width() / settings.current_w * 2
                x = - w / 2
                h = text_surf.get_height() / settings.current_h * 2
                y = 0.7
                blit(x, y, w, h, text_surf)

            pygame.display.flip()

            clock.tick(30)

    def high_scores(self, scores: dict[str, int]):
        clock = pygame.time.Clock()
        n = len(scores)
        while True:
            for event in self.poll_events():
                if event == Menu.Action.QUIT:
                    return Command.EXIT
                if event == Menu.Action.BACK:
                    return Command.BACK

            glClear(GL_COLOR_BUFFER_BIT)

            for i in range(n):
                text = list(scores.keys())[i] + ' : %.2f' % list(scores.values())[i]
                text_surf = font.render(text, False, (255, 255, 255))
                w = text_surf.get_width() / settings.current_w * 2
                x = - w / 2
                h = text_surf.get_height() / settings.current_h * 2
                y = h + (20 + text_surf.get_height()) * (n / 2 - i) / settings.current_h * 2
                blit(x, y, w, h, text_surf)

            pygame.display.flip()

            clock.tick(30)

    def name(self, player_name: str):
        position = 0
        clock = pygame.time.Clock()
        options = ('Name', 'Team')
        n = len(options)
        while True:
            for event in self.poll_events():
                if event == Menu.Action.BACK:
                    return Command.BACK
                elif event == Menu.Action.QUIT:
                    return Command.EXIT
                elif event == Menu.Action.ENTER:
                    return Command.BACK if player_name == '' else player_name
                elif event == Menu.Action.DOWN:
                    position = min(position + 1, n - 1)
                elif event == Menu.Action.UP:
                    position = max(position - 1, 0)
                elif event == Menu.Action.DELETE:
                    if position == options.index('Name'):
                        player_name = player_name[:-1]
                elif event == Menu.Action.UNICODE:
                    if position == options.index('Name'):
                        player_name += self.unicode.pop().upper()

            glClear(GL_COLOR_BUFFER_BIT)

            for i in range(n):
                text = ('→ ' + options[i] + ' : ', '  ' + options[i] + ' : ')[i != position]
                if i == options.index('Name'):
                    text += player_name
                text_surf = font.render(text, False, (255, 255, 255))
                w = text_surf.get_width() / settings.current_w * 2
                x = -0.3
                h = text_surf.get_height() / settings.current_h * 2
                y = h + (20 + text_surf.get_height()) * (n / 2 - i) / settings.current_h * 2
                blit(x, y, w, h, text_surf)
            pygame.display.flip()

            clock.tick(30)

    def credits(self):
        clock = pygame.time.Clock()
        credit = ['GAME_NAME', 'Director : Eugene', 'Credits music by LHS']
        pygame.mixer.music.load(file_path('lhs_rld1.xm'))
        pygame.mixer.music.play(-1)
        t = 0
        i = -1
        while True:
            for event in self.poll_events():
                if event == Menu.Action.BACK or event == Menu.Action.ENTER:
                    return Command.BACK
                elif event == Menu.Action.QUIT:
                    return Command.EXIT

            if t == 0:
                i += 1
                i %= len(credit) + 2
                glClear(GL_COLOR_BUFFER_BIT)
                if i < len(credit):
                    text_surf = font.render(credit[i], False, (255, 255, 255))
                    w = text_surf.get_width() / settings.current_w * 2
                    h = text_surf.get_height() / settings.current_h * 2
                    x = - w / 2
                    y = h
                    blit(x, y, w, h, text_surf)

                pygame.display.flip()

            t += clock.tick(30)
            if t >= 2000:
                t = 0


def blit(x, y, w, h, surf):
    vertex_data = (ctypes.c_float * 16)(
        x, y, x + w, y, x + w, y + h, x, y + h,
        0, 0, 1, 0, 1, 1, 0, 1
    )
    glBufferSubData(GL_ARRAY_BUFFER, 0, 16 * sizeof(c_float), vertex_data)
    glBindTexture(GL_TEXTURE_2D, image_texture)
    image_data = pygame.image.tostring(surf, "RGBA", True)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, surf.get_width(), surf.get_height(), 0, GL_RGBA,
                 GL_UNSIGNED_BYTE, image_data)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glDrawArrays(GL_TRIANGLE_FAN, 0, 4)
    glInvalidateBufferData(vbo)
    glBindTexture(GL_TEXTURE_2D, 0)
