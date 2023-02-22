import time
from common import *
from utils import image

font = TTF_OpenFont(file_path('menu_font.ttf'), 30)

image_texture = glGenTextures(1)
credits_music = Mix_LoadWAV(file_path('lhs_rld1.xm'))
menu_music = Mix_LoadWAV(file_path('menu.mp3'))


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
        event = SDL_Event()
        while SDL_PollEvent(byref(event)) > 0:
            common_event(event)

            keydown = event.type == SDL_KEYDOWN
            joy_axis_motion = settings.joystick and event.type == SDL_JOYAXISMOTION
            joy_button_down = settings.joystick and event.type == SDL_JOYBUTTONDOWN
            if joy_axis_motion:
                jaxis = event.jaxis.axis
                jvalue = event.jaxis.value / 32768
            if joy_button_down:
                jbutton = event.jbutton.button

            if (keydown and event.key.keysym.sym == SDLK_ESCAPE) or (joy_button_down and jbutton == 1):
                actions.append(Menu.Action.BACK)
            elif (keydown and event.key.keysym.sym == SDLK_BACKSPACE) or (joy_button_down and jbutton == 2):
                actions.append(Menu.Action.DELETE)
            elif keydown and event.key.keysym.sym == SDLK_DOWN or \
                    joy_axis_motion and jaxis == 1 and jvalue > self.deadzone and self.joy_delay == 0 \
                    and abs(jvalue) > last_joy_value:
                actions.append(Menu.Action.DOWN)
                if joy_axis_motion:
                    self.joy_delay = self.JOYSTICK_DELAY
            elif keydown and event.key.keysym.sym == SDLK_UP or \
                    joy_axis_motion and jaxis == 1 and jvalue < -self.deadzone and self.joy_delay == 0 \
                    and abs(jvalue) > last_joy_value:
                actions.append(Menu.Action.UP)
                if joy_axis_motion:
                    self.joy_delay = self.JOYSTICK_DELAY
            elif keydown and event.key.keysym.sym in (SDLK_RETURN, SDLK_KP_ENTER) \
                    or joy_button_down and jbutton == 0:
                actions.append(Menu.Action.ENTER)
            elif event.type == SDL_QUIT:
                actions.append(Menu.Action.QUIT)
            elif event.type == SDL_WINDOWEVENT:
                if event.window.event in (SDL_WINDOWEVENT_RESIZED, SDL_WINDOWEVENT_SIZE_CHANGED):
                    settings.update_screen(event.window.data1, event.window.data2)
            elif keydown and not SDL_GetModState() & (KMOD_SHIFT | KMOD_CTRL | KMOD_ALT):
                actions.append(Menu.Action.UNICODE)
                try:
                    self.unicode.append(chr(event.key.keysym.sym))
                except ValueError:
                    ...
            if event.type == SDL_JOYAXISMOTION and jaxis == 1:
                last_joy_value = abs(jvalue) + 0.1
        return actions

    def main(self, info: dict):
        player_name = info['player_name']
        position = 0
        options = ('Start', 'High scores', 'Credits', 'Exit')
        Mix_HaltChannel(-1)
        Mix_FadeInChannel(-1, menu_music, -1, 100)
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
                        Mix_HaltChannel(-1)
                        Mix_FadeInChannel(-1, menu_music, -1, 100)
                    elif position == options.index('Exit'):
                        return Command.EXIT
                if event == Menu.Action.DOWN:
                    position = min(position + 1, n - 1)
                if event == Menu.Action.UP:
                    position = max(position - 1, 0)

            glClear(GL_COLOR_BUFFER_BIT)

            for i in range(n):
                text = ('→ ' + options[i] + ' ←', options[i])[i != position]
                surf = TTF_RenderUTF8_Blended(font, text.encode(), SDL_Color()).contents
                w = surf.w / settings.current_w * 2
                x = - w / 2
                h = surf.h / settings.current_h * 2
                y = h + (20 + surf.h) * (n / 2 - i) / settings.current_h * 2 - 0.1

                blit(x, y, w, h, surf)

            if info['player_score'] > 0:
                text = 'New best for ' + \
                       info['player_name'] + \
                       ' : ' if info['player_score'] == info['scores'][info['player_name']] else ''
                text += str(round(info['player_score'], 2))
                surf = TTF_RenderUTF8_Blended(font, text.encode(), SDL_Color()).contents
                w = surf.w / settings.current_w * 2
                x = - w / 2
                h = surf.h / settings.current_h * 2
                y = 0.7
                blit(x, y, w, h, surf)

            SDL_GL_SwapWindow(window)
            SDL_Delay(20)

    def high_scores(self, scores: dict[str, int]):
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
                surf = TTF_RenderUTF8_Blended(font, text.encode(), SDL_Color()).contents
                w = surf.w / settings.current_w * 2
                x = - w / 2
                h = surf.h / settings.current_h * 2
                y = h + (20 + surf.h) * (n / 2 - i) / settings.current_h * 2
                blit(x, y, w, h, surf)

            SDL_GL_SwapWindow(window)
            SDL_Delay(20)

    def name(self, player_name: str):
        position = 0
        options = ('Name',)
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
                        try:
                            player_name += self.unicode.pop().upper()
                        except IndexError:
                            ...

            glClear(GL_COLOR_BUFFER_BIT)

            for i in range(n):
                text = ('→ ' + options[i] + ' : ', '  ' + options[i] + ' : ')[i != position]
                if i == options.index('Name'):
                    text += player_name
                surf = TTF_RenderUTF8_Blended(font, text.encode(), SDL_Color()).contents
                w = surf.w / settings.current_w * 2
                x = -0.3
                h = surf.h / settings.current_h * 2
                y = h + (20 + surf.h) * (n / 2 - i) / settings.current_h * 2
                blit(x, y, w, h, surf)

            SDL_GL_SwapWindow(window)
            SDL_Delay(20)

    def credits(self):
        credit = ['GAME_NAME', 'Director : Eugene']
        Mix_HaltChannel(-1)
        Mix_PlayChannel(-1, credits_music, -1)
        i = 0
        last_i = -1
        while True:
            for event in self.poll_events():
                if event == Menu.Action.BACK or event == Menu.Action.ENTER:
                    return Command.BACK
                elif event == Menu.Action.QUIT:
                    return Command.EXIT
            if last_i != int(i):
                last_i = int(i)
            glClear(GL_COLOR_BUFFER_BIT)
            if i < len(credit):
                text = credit[last_i]
                surf = TTF_RenderUTF8_Blended(font, text.encode(), SDL_Color()).contents
                w = surf.w / settings.current_w * 2
                h = surf.h / settings.current_h * 2
                x = - w / 2
                y = h
                blit(x, y, w, h, surf)
            i += 0.01
            if i >= len(credit) + 2:
                i = 0

            SDL_GL_SwapWindow(window)
            SDL_Delay(20)

def power_two_floor(val):
    return int(2 ** int(math.log(val, 2)))

def blit(x, y, w, h, surf: SDL_Surface):
    surf = image.convert_to_rgba32(surf)
    vertex_data = (ctypes.c_float * 16)(
        x, y, x + w, y, x + w, y + h, x, y + h,
        0, 0, 1, 0, 1, 1, 0, 1
    )

    glBufferSubData(GL_ARRAY_BUFFER, 0, 16 * sizeof(c_float), vertex_data)
    glBindTexture(GL_TEXTURE_2D, image_texture)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, surf.w, surf.h, 0, GL_RGBA, GL_UNSIGNED_BYTE, c_void_p(surf.pixels))
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glDrawArrays(GL_TRIANGLE_FAN, 0, 4)
    glBindTexture(GL_TEXTURE_2D, 0)
