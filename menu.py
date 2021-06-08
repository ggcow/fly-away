import time

import numpy as np
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
from opengl import menu_vao, menu_vbo, tex_vao, tex_vbo
from opengl import menu_shader_program, tex_shader_program

font = pygame.font.Font(file_path('menu_font.ttf'), 30)


class Action(Enum):
    BACK = 1
    ENTER = 2
    QUIT = 3
    UP = 4
    DOWN = 5
    DELETE = 6
    UNICODE = 7


image_texture = glGenTextures(1)


class Menu:
    def __init__(self):
        self.deadzone = 0.7
        self.JOYSTICK_DELAY = 0.130
        self.joy_delay = self.JOYSTICK_DELAY
        self.time = time.monotonic()
        self.unicode = []

    def get_unicode(self):
        return self.unicode.pop()

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
                actions.append(Action.BACK)
            elif (keydown and event.key == K_BACKSPACE) or (joy_button_down and event.button == 2):
                actions.append(Action.DELETE)
            elif keydown and event.key == K_DOWN or \
                    joy_axis_motion and event.axis == 1 and event.value > self.deadzone and self.joy_delay == 0 \
                    and abs(event.value) > last_joy_value:
                actions.append(Action.DOWN)
                if joy_axis_motion:
                    self.joy_delay = self.JOYSTICK_DELAY
            elif keydown and event.key == K_UP or \
                    joy_axis_motion and event.axis == 1 and event.value < -self.deadzone and self.joy_delay == 0 \
                    and abs(event.value) > last_joy_value:
                actions.append(Action.UP)
                if joy_axis_motion:
                    self.joy_delay = self.JOYSTICK_DELAY
            elif keydown and event.key in (K_RETURN, K_KP_ENTER) or joy_button_down and event.button == 0:
                actions.append(Action.ENTER)
            elif event.type == pygame.QUIT:
                actions.append(Action.QUIT)
            elif event.type == pygame.VIDEORESIZE:
                settings.update_screen(event.w, event.h)
                glViewport(0, 0, settings.current_w, settings.current_h)
            elif keydown and not pygame.key.get_mods() & (KMOD_SHIFT | KMOD_CTRL | KMOD_ALT):
                actions.append(Action.UNICODE)
                self.unicode.append(event.unicode)

            if event.type == pygame.JOYAXISMOTION and event.axis == 1:
                last_joy_value = abs(event.value) + 0.1
        return actions


def menu(player: dict[str, int]):
    pygame.key.set_repeat(500, 70)
    name = player['name']
    m = Menu()
    pygame.font.init()
    position = 0
    clock = pygame.time.Clock()
    options = ('Start', 'Credits', 'Exit')
    pygame.mixer.music.load(file_path('menu.mp3'))
    pygame.mixer.music.set_volume(MUSIC_VOLUME / 2)
    pygame.mixer.music.play(-1, fade_ms=100)
    n = len(options)
    while True:
        for event in m.poll_events():
            if event == Action.QUIT:
                return Command.EXIT
            if event == Action.ENTER:
                if position == options.index('Start'):
                    name = menu_name(name if not isinstance(name, Command) else '')
                    if name != Command.BACK:
                        return name
                elif position == options.index('Credits'):
                    if menu_credits() == Command.EXIT:
                        return Command.EXIT
                    pygame.mixer.music.load(file_path('menu.mp3'))
                    pygame.mixer.music.set_volume(MUSIC_VOLUME / 2)
                    pygame.mixer.music.play(-1, fade_ms=100)
                elif position == options.index('Exit'):
                    return Command.EXIT
            if event == Action.DOWN:
                position = min(position + 1, n - 1)
            if event == Action.UP:
                position = max(position - 1, 0)

        menu_clear()

        for i in range(n):
            text = ('→ ' + options[i] + ' ←', options[i])[i != position]
            text_surf = font.render(text, False, (255, 255, 255))
            w = text_surf.get_width() / settings.current_w * 2
            x = - w / 2
            h = text_surf.get_height() / settings.current_h * 2
            y = h + (20 + text_surf.get_height()) * (n / 2 - i) / settings.current_h * 2

            blit(x, y, w, h, text_surf)

        if player['score'] > 0:
            text = 'New best for ' + str(player['name']) + ' : ' if player['new_best'] else ''
            text_surf = font.render(text + str(round(player['score'], 2)), False, (255, 255, 255))
            w = text_surf.get_width() / settings.current_w * 2
            x = - w / 2
            h = text_surf.get_height() / settings.current_h * 2
            y = 0.7
            blit(x, y, w, h, text_surf)

        pygame.display.flip()

        clock.tick(30)


def menu_name(name: str):
    position = 0
    clock = pygame.time.Clock()
    options = ('Name', 'Team')
    n = len(options)
    m = Menu()
    while True:
        for event in m.poll_events():
            if event == Action.BACK:
                return Command.BACK
            elif event == Action.QUIT:
                return Command.EXIT
            elif event == Action.ENTER:
                return Command.BACK if name == '' else name
            elif event == Action.DOWN:
                position = min(position + 1, n - 1)
            elif event == Action.UP:
                position = max(position - 1, 0)
            elif event == Action.DELETE:
                if position == options.index('Name'):
                    name = name[:-1]
            elif event == Action.UNICODE:
                if position == options.index('Name'):
                    name += m.get_unicode().upper()

        menu_clear()

        for i in range(n):
            text = ('→ ' + options[i] + ' : ', '  ' + options[i] + ' : ')[i != position]
            if i == options.index('Name'):
                text += name
            text_surf = font.render(text, False, (255, 255, 255))
            w = text_surf.get_width() / settings.current_w * 2
            x = -0.3
            h = text_surf.get_height() / settings.current_h * 2
            y = h + (20 + text_surf.get_height()) * (n / 2 - i) / settings.current_h * 2
            blit(x, y, w, h, text_surf)
        pygame.display.flip()

        clock.tick(30)


def menu_credits():
    clock = pygame.time.Clock()
    m = Menu()
    credit = ['GAME_NAME', 'Director : Eugène', 'Music by LHS']
    pygame.mixer.music.load(file_path('lhs_rld1.xm'))
    pygame.mixer.music.play(-1)
    t = 0
    i = -1
    while True:
        for event in m.poll_events():
            if event == Action.BACK or event == Action.ENTER:
                return Command.BACK
            elif event == Action.QUIT:
                return Command.EXIT

        if t == 0:
            i += 1
            i %= len(credit) + 2
            menu_clear()
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
    glBindBuffer(GL_ARRAY_BUFFER, tex_vbo)
    vertex_data = np.array([
        x, y, 0, 0,
        x + w, y, 1, 0,
        x + w, y + h, 1, 1,
        x, y + h, 0, 1
    ], np.float32)
    glBufferData(GL_ARRAY_BUFFER, vertex_data, GL_DYNAMIC_DRAW)
    glBindTexture(GL_TEXTURE_2D, image_texture)
    image_data = pygame.image.tostring(surf, "RGBA", True)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, surf.get_width(), surf.get_height(), 0, GL_RGBA,
                 GL_UNSIGNED_BYTE, image_data)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glUseProgram(tex_shader_program)
    glEnable(GL_TEXTURE_2D)
    glBindVertexArray(tex_vao)
    glDrawArrays(GL_TRIANGLE_FAN, 0, 4)
    glBindVertexArray(0)
    glInvalidateBufferData(tex_vbo)
    glBindTexture(GL_TEXTURE_2D, 0)
    glBindBuffer(GL_ARRAY_BUFFER, 0)


def menu_clear():
    glDisable(GL_TEXTURE_2D)
    glDisable(GL_BLEND)
    glUseProgram(menu_shader_program)
    glBindBuffer(GL_ARRAY_BUFFER, menu_vbo)
    glBindVertexArray(menu_vao)
    glDrawArrays(GL_TRIANGLE_FAN, 0, 4)
    glBindVertexArray(0)
    glBindBuffer(GL_ARRAY_BUFFER, 0)
