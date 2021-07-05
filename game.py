import time
import levels
from levels.city import City
from levels.mountains import Mountains
from entities import ressources
from common import *
from OpenGL.GL import *

new_best_sound = Mix_LoadWAV(file_path('win.wav'))
best_sound_played = False
start_time = time.time()


def game(best: int) -> float:
    global start_time
    start_time = time.time()
    ressources.resize()
    hp = 3
    for level in (City(),):
        command = play(level, best, hp)
        if command == Command.EXIT:
            return 0
        if command == Command.BACK:
            break
        hp = level.plane.hp

    return time.time() - start_time


def play(level: levels.Level, best: int, hp: int) -> Command:
    global best_sound_played, start_time
    level_time = time.time()
    frame_time = 0
    frames = 0
    delta = 1000 / 61
    last_time = start_time
    joy_value = Vec2(0, 0)

    event = SDL_Event()
    level.start(hp)

    while True:
        while SDL_PollEvent(byref(event)) > 0:
            common_event(event)

            if event.type == SDL_KEYDOWN:
                if event.key.keysym.sym == SDLK_ESCAPE:
                    return Command.BACK
            elif event.type == SDL_QUIT:
                return Command.EXIT
            elif event.type == SDL_JOYAXISMOTION:
                if event.jaxis.axis == 0:
                    joy_value.x = event.jaxis.value / 32768
                elif event.jaxis.axis == 1:
                    joy_value.y = event.jaxis.value / 32768
            elif event.type == SDL_WINDOWEVENT:
                if event.window.event in (SDL_WINDOWEVENT_RESIZED, SDL_WINDOWEVENT_SIZE_CHANGED):
                    settings.update_screen(event.window.data1, event.window.data2)
                    ressources.resize()
                    level.resize()

        keys = SDL_GetKeyboardState(ctypes.c_int(0))
        if level.update(delta, keys, joy_value):
            return Command.BACK

        t = time.time()

        if not best_sound_played and t - start_time > best:
            Mix_PlayChannel(-1, new_best_sound, 0)
            best_sound_played = True

        if t - level_time >= 20:
            return Command.NEXT

        frames += 1

        time_delta = t - last_time
        frame_time += time_delta
        if frame_time >= 1:
            frame_time = 0
            print('FPS :', frames)
            frames = 0
        last_time = t
