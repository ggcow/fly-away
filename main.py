import ast
import menu
import game
from common import *


def main():
    player_name = ''
    player_score = 0.
    main_menu = menu.Menu().main

    if not os.path.exists('scores.txt'):
        with open('scores.txt', 'w') as f:
            f.write('{}')
        scores = {}
    else:
        with open('scores.txt', 'r') as f:
            scores = ast.literal_eval(f.readline())

    while True:
        player_name = main_menu({
            'player_name': player_name,
            'player_score': player_score,
            'scores': scores
        })

        if player_name == Command.EXIT:
            break
        try:
            best_score = list(scores.values())[0]
        except IndexError:
            best_score = 0
        player_score = game.game(best_score)
        if player_score == 0:
            break

        print(player_name, ':', player_score)
        if player_score > scores.get(player_name, 0):
            scores[player_name] = player_score
            scores = dict(sorted(
                scores.items(),
                key=lambda item: item[1],
                reverse=True
            ))
            with open('scores.txt', 'w') as f:
                f.write(scores.__str__())

    if settings.joystick:
        SDL_JoystickClose(settings.joy)
    SDL_GL_DeleteContext(context)
    Mix_CloseAudio()
    Mix_Quit()
    TTF_Quit()
    IMG_Quit()
    SDL_Quit()


if __name__ == '__main__':
    main()
