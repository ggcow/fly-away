import time

import pygame
from pygame.locals import (
    K_ESCAPE,
    K_DOWN,
    K_UP,
    K_RETURN,
    K_BACKSPACE,
)
from enum import Enum
from common import (
    screen,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    Command
)

font = pygame.font.Font('menu_font.ttf', 30)


class Action(Enum):
    BACK = 1
    ENTER = 2
    QUIT = 3
    UP = 4
    DOWN = 5
    DELETE = 6
    UNICODE = 7


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
            keydown = event.type == pygame.KEYDOWN
            joy_axis_motion = pygame.joystick.get_init() and event.type == pygame.JOYAXISMOTION
            joy_button_down = pygame.joystick.get_init() and event.type == pygame.JOYBUTTONDOWN

            if (keydown and event.key == K_ESCAPE) or (joy_button_down and event.button == 1):
                actions.append(Action.BACK)
            elif (keydown and event.key == K_BACKSPACE) or (joy_button_down and event.button == 2):
                actions.append(Action.DELETE)
            elif keydown and event.key == K_DOWN or \
                    joy_axis_motion and event.axis == 1 and event.value > deadzone and self.joy_delay == 0 \
                    and abs(event.value) > last_joy_value:
                actions.append(Action.DOWN)
                if joy_axis_motion:
                    self.joy_delay = JOYSTICK_DELAY
            elif keydown and event.key == K_UP or \
                    joy_axis_motion and event.axis == 1 and event.value < -deadzone and self.joy_delay == 0 \
                    and abs(event.value) > last_joy_value:
                actions.append(Action.UP)
                if joy_axis_motion:
                    self.joy_delay = JOYSTICK_DELAY
            elif keydown and event.key == K_RETURN or joy_button_down and event.button == 0:
                actions.append(Action.ENTER)
            elif event.type == pygame.QUIT:
                actions.append(Action.QUIT)
            elif keydown:
                actions.append(Action.UNICODE)
                self.unicode.append(event.unicode)

            if event.type == pygame.JOYAXISMOTION and event.axis == 1:
                last_joy_value = abs(event.value) + 0.1
        return actions


def menu():
    m = Menu()
    pygame.font.init()
    position = 0
    clock = pygame.time.Clock()
    options = ('Start', 'Exit')
    n = len(options)
    while True:
        for event in m.poll_events():
            if event == Action.QUIT:
                return Command.EXIT
            if event == Action.ENTER:
                if position == options.index('Start'):
                    name = menu_name()
                    if name != Command.BACK:
                        return name
                elif position == options.index('Exit'):
                    return Command.EXIT
            if event == Action.DOWN:
                position = min(position + 1, n - 1)
            if event == Action.UP:
                position = max(position - 1, 0)

        screen.fill((0, 0, 0))

        for i in range(n):
            text = ('→ ' + options[i] + ' ←', options[i])[i != position]
            text_surf = font.render(text, False, (255, 255, 255))
            w = SCREEN_WIDTH / 2
            h = SCREEN_HEIGHT / 2 - (20 + text_surf.get_height()) * (n / 2 - i)
            screen.blit(text_surf, (w - text_surf.get_width() / 2,
                                    h - text_surf.get_height() / 2))

        pygame.display.flip()

        clock.tick(30)


def menu_name():
    position = 0
    clock = pygame.time.Clock()
    options = ('Name', 'Team')
    name = ''
    n = len(options)
    m = Menu()
    while True:
        for event in m.poll_events():
            if event == Action.BACK:
                return Command.BACK
            elif event == Action.QUIT:
                return Command.EXIT
            elif event == Action.ENTER:
                return name
            elif event == Action.DOWN:
                position = min(position + 1, n - 1)
            elif event == Action.UP:
                position = max(position - 1, 0)
            elif event == Action.DELETE:
                if position == options.index('Name'):
                    name = name[:-1]
            elif event == Action.UNICODE:
                if position == options.index('Name'):
                    name += m.get_unicode()

        screen.fill((0, 0, 0))

        for i in range(n):
            text = ('→ ' + options[i] + ' : ', '  ' + options[i] + ' : ')[i != position]
            if i == options.index('Name'):
                text += name
            text_surf = font.render(text, False, (255, 255, 255))
            w = SCREEN_WIDTH / 2
            h = SCREEN_HEIGHT / 2 - (20 + text_surf.get_height()) * (n / 2 - i)
            screen.blit(text_surf, (w - 100,
                                    h - text_surf.get_height() / 2))
        pygame.display.flip()

        clock.tick(30)

