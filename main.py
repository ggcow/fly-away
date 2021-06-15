import ast
import menu
import game
from common import *


def main():
    player_name = ''

    if not os.path.exists('scores.txt'):
        with open('scores.txt', 'w') as f:
            f.write('{}')
        scores = {}
    else:
        with open('scores.txt', 'r') as f:
            scores = ast.literal_eval(f.readline())

    player_score: int = 0
    m = menu.Menu()

    while True:
        player_name = m.main({'player_name': player_name, 'player_score': player_score, 'scores': scores})
        if player_name != Command.EXIT:
            try:
                best_score = list(scores.values())[0]
            except IndexError:
                best_score = 0
            player_score = game.game(best_score)
        else:
            break

        print(str(player_name) + " : " + str(player_score))
        if player_score > scores.get(player_name, 0):
            scores[player_name] = player_score
            scores = dict(sorted(scores.items(), key=lambda item: item[1], reverse=True))
            with open('scores.txt', 'w') as f:
                f.write(scores.__str__())

    SDL_GL_DeleteContext(context)
    Mix_CloseAudio()
    Mix_Quit()
    TTF_Quit()
    IMG_Quit()
    SDL_Quit()


if __name__ == '__main__':
    main()
